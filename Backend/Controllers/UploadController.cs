namespace AI_spotter.Controllers;

using Microsoft.AspNetCore.Mvc;
using AI_spotter.PublicClasses;



[ApiController]
[Route("api/[controller]/[action]")]
public class UploadController : ControllerBase{
    [HttpPost]
    public IActionResult UploadVideo(IFormFile video){
        return Ok(new UploadHandler().Upload(video));
    }
}


