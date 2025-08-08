namespace AI_spotter.Controllers;

using AI_spotter.Models;
using AI_spotter.Services;
using Microsoft.AspNetCore.Mvc;
using AI_spotter.PublicClasses;



[ApiController]
[Route("[controller]")]
public class VideoController : ControllerBase{
    UploadHandler handleHerVideo = new UploadHandler();
    public VideoController(){
    }

    [HttpGet]
    public ActionResult<List<Video>> GetAll() => VideoService.GetAll();


    [HttpGet("{id}")]
    public ActionResult<Video> Get(int id){
        var video = VideoService.Get(id);
        if (video == null){
            return NotFound();
        }
        return video;
    }



    [HttpPut]
    public IActionResult CreateVerdict(int id){
        path = video.path;
        // Call on FASTAPI, with path to video
        // Await response
        // Save JSONRESPONSE in database
        // GET(response)
        analyze.add(response)
        return Success
    }

    def make_verdict(path):
        return "{verdict: bad}"

    def process_video(video):
        // ....
        // ...
        retrun response

    def API_CALL(path):
        verdict = make_verdict(path)
        process_video()
        retrun Response(header, verdict)


    localhost/FastApi/PostVerdict{string path}
        ->      retrun JSONRESPONSE {"verdict": "bad"}


    [HttpPost]
    public IActionResult Create(IFormFile video){
        (bool IsSuccess, string response) videoResponse = handleHerVideo.Upload(video);
        if (!videoResponse.IsSuccess){
            return BadRequest(videoResponse.response);
        }
        Video returnedVideo = new Video(){Id = -1, Name = videoResponse.response, 
                Path = Path.Combine(Path.Combine(Directory.GetCurrentDirectory(), "Videos"), videoResponse.response)};
        VideoService.Add(returnedVideo);
        return CreatedAtAction(nameof(Get), new { id = returnedVideo.Id }, returnedVideo);
    }

// Imagine we wont need to PUT a video, atlest not for now
//    [HttpPut("{id}")]
//    public IActionResult Update(int id, Video video){
//        if (id != video.Id){
//            return BadRequest();
//        }
//        Video? prevVid = VideoService.Get(id);
//        if (prevVid is null){
//            return NotFound();
//        }
//        VideoService.Update(video);
//        return NoContent();
//    }

    [HttpDelete("{id}")]
    public IActionResult Delete(int id){
        Video? video = VideoService.Get(id);
        if (video is null){
            return NotFound();
        }
        if (System.IO.File.Exists(video.Path)){
            System.IO.File.Delete(video.Path);
            VideoService.Delete(id);
            return NoContent();
        }
        return StatusCode(500);
    }
}
