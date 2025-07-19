namespace AI_spotter.Services;
using AI_spotter.Models;

public class VideoService(){
    static List<Video> Videos { get; }

    static int currId = 3;
    static VideoService(){
        Videos = new List<Video>{
        new Video{Id = 1, Path = "temp/Vid_1"},
        new Video{Id = 2, Path = "temp/Vid_2"}
        };
    }

    public static List<Video> GetAll() => Videos;

    public static Video? Get(int id) => Videos.FirstOrDefault<Video>(v => v.Id == id);

    public static void Add(Video video){
        video.Id = currId++;
        Videos.Add(video);
    }

    public static void Update(Video video){
        var prevVid = Videos.Find(v => v.Id == video.Id);
        if (prevVid is null){
            return;
        }
        Videos[Videos.IndexOf(prevVid)] = video;
    }

    public static void Delete(int id){
        Video? video = Get(id);
        if (video is null){
            return;
        }
        Videos.Remove(video);
    }
}
