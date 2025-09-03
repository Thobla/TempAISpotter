namespace AI_spotter.Controllers;

using AI_spotter.Models;
using AI_spotter.Services;
using Microsoft.AspNetCore.Mvc;
using AI_spotter.PublicClasses;
using System.Net.Http;
using System.IO; // ← for Path / Directory

public interface IAiClientConnect{
    HttpClient AiClient { get; }
    Task<HttpResponseMessage> Connect(string path);
}

public class AiClientConnect : IAiClientConnect{
    public HttpClient AiClient { get; }
    public AiClientConnect(HttpClient client){
        AiClient = client;
    }
    public async Task<HttpResponseMessage> Connect(string path){
        try{
            using HttpResponseMessage response = await AiClient.GetAsync($"http://localhost:8000/verdict?path={path}");
            response.EnsureSuccessStatusCode();
            string responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseBody);
            return response;
        }
        catch (HttpRequestException e){
            Console.WriteLine("\nException caught");
            Console.WriteLine("Exception message: {0}", e.Message);
            return new HttpResponseMessage(System.Net.HttpStatusCode.NoContent);
        }
    }
}

[ApiController]
[Route("[controller]")]
public class VideoController : ControllerBase{
    private readonly IAiClientConnect AiClient;
    private readonly UploadHandler handleHerVideo = new UploadHandler();

    public VideoController(IAiClientConnect aiClient){
        AiClient = aiClient;
    }

    [HttpGet]
    public ActionResult<List<Video>> GetAll() => VideoService.GetAll();

    [HttpGet("{id}")]
    public ActionResult<Video> Get(int id){
        var video = VideoService.Get(id);
        if (video == null) return NotFound();
        return video;
    }

    [HttpGet("aiApi/{aiMethod}/{id}")]
    public async Task<IActionResult> GetAI(string aiMethod, int id){
        try{
            var path = VideoService.Get(id)?.Path;
            if (path == null) throw new NullReferenceException("id or path is null");

            // HttpResponseMessage result = await AiClient.Connect(path);
            HttpResponseMessage result = await AiClient.AiClient.GetAsync($"http://localhost:8000/verdict?path={path}");
            if (result.IsSuccessStatusCode){
                Console.WriteLine("got results");
                return Ok(await result.Content.ReadAsStringAsync());
            }
            return StatusCode((int)result.StatusCode, result.ReasonPhrase);
        }
        catch (HttpRequestException e){
            return StatusCode(500, $"Internal Server Error: {e.Message}");
        }
    }

    // ---- CREATE -------------------------------------------------------------

    [HttpPost]
    [Consumes("multipart/form-data")]
    public IActionResult Create([FromForm] IFormFile video){
        var videoResponse = handleHerVideo.Upload(video);
        if (!videoResponse.IsSuccess) return BadRequest(videoResponse.Response);

        var storedName = videoResponse.Response; // GUID.ext saved on disk
        var fullPath   = Path.Combine(Directory.GetCurrentDirectory(), "Videos", storedName);

        var returnedVideo = new Video{
            Id = -1,
            Name = storedName,             // stored filename used for serving
            OriginalName = video.FileName, // pretty/original filename
            Path = fullPath
        };

        VideoService.Add(returnedVideo);
        return CreatedAtAction(nameof(Get), new { id = returnedVideo.Id }, returnedVideo);
    }

    // ---- UPDATE (overwrite file; keep or update OriginalName) ---------------

    [HttpPut("{id}")]
    [Consumes("multipart/form-data")]
    public IActionResult Update([FromForm] IFormFile newVideo, int id){
        var existing = VideoService.Get(id);
        if (existing == null) return NotFound();

        // Overwrite the SAME stored file name on disk
        var result = handleHerVideo.Upload(newVideo, existing.Name);
        if (!result.IsSuccess) return BadRequest(result.Response);

        // Option A: keep previous OriginalName (do nothing)
        // Option B: update to new uploaded filename:
        // existing.OriginalName = newVideo.FileName;

        // Path unchanged (same stored name)
        VideoService.Update(existing);

        return CreatedAtAction(nameof(Get), new { id = existing.Id }, existing);
    }

    // ---- DELETE -------------------------------------------------------------

    [HttpDelete("{id}")]
    public IActionResult Delete(int id){
        var video = VideoService.Get(id);
        if (video is null) return NotFound();

        if (System.IO.File.Exists(video.Path)){
            System.IO.File.Delete(video.Path);
            VideoService.Delete(id);
            return NoContent();
        }
        return StatusCode(500);
    }
}
