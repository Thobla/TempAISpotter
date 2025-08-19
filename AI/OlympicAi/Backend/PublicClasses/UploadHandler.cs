namespace AI_spotter.PublicClasses
{
    public class UploadHandler{

        public (bool IsSuccess, string Response) Upload(IFormFile video){
            //extension
            List<string> validExtensions = new List<string>(){".mp4", ".gif"};
            string extension = Path.GetExtension(video.FileName);
            if (!validExtensions.Contains(extension)){
                return ( false, $"({extension}) is not a valid extension, valid extensions are ({string.Join(',', validExtensions)})");
            }
            //Filesize
            long size = video.Length;
            long maxMegaBytes = 100;
            if (size > (maxMegaBytes * 1024 * 1024)){
                return ( false, $"Maximum file size is ({maxMegaBytes})");
            }
            //name changing
            string fileName = Guid.NewGuid().ToString() + extension;
            string path = Path.Combine(Directory.GetCurrentDirectory(), "Videos");



            using FileStream stream = new FileStream(Path.Combine(path, fileName), FileMode.Create);
            video.CopyTo(stream);

            return ( true, fileName);
        }
    }
}
