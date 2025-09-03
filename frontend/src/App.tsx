import { useState } from "react";
import styles from "./App.module.css";

type Video = {
    id: number;
    path?: string | null;
    name?: string | null;           // stored GUID name
    originalName?: string | null;   // pretty name
};

export default function App() {
    const [video, setVideo] = useState<Video | null>(null);
    const [verdict, setVerdict] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [busy, setBusy] = useState(false);

    async function handleUploadEl(input: HTMLInputElement) {
        const file = input.files?.[0];
        if (!file) return;

        const fd = new FormData();
        fd.append("video", file);

        try {
            setBusy(true);
            setError(null);
            setVerdict(null);

            const res = await fetch("/Video", { method: "POST", body: fd });
            if (!res.ok) throw new Error(await res.text());
            const data: Video = await res.json();
            setVideo(data);
        } catch (err: any) {
            setError(err.message ?? String(err));
        } finally {
            input.value = "";
            setBusy(false);
        }
    }

    async function handleAnalysis() {
        if (!video) return;
        try {
            setBusy(true);
            setError(null);

            const res = await fetch(`/Video/aiApi/squat/${video.id}`);
            if (!res.ok) throw new Error(await res.text());
            const text = await res.text();
            setVerdict(text);
        } catch (err: any) {
            setError(err.message ?? String(err));
        } finally {
            setBusy(false);
        }
    }

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>AI Spotter</h1>

            <div style={{ marginBottom: "1rem" }}>
                <input
                    type="file"
                    accept="video/mp4,video/gif"
                    onChange={(e) => handleUploadEl(e.currentTarget)}
                />
            </div>

            {busy && <p>Working…</p>}
            {error && <p style={{ color: "crimson" }}>{error}</p>}

            {video && (
                <div className={styles.card}>
                    <p className={styles.uploadInfo}>
                        <strong>Uploaded:</strong> {video.originalName ?? video.name} —{" "}
                        <strong>ID:</strong> {video.id}
                    </p>
                    <button
                        onClick={handleAnalysis}
                        disabled={busy}
                        className={styles.button}
                    >
                        Do Analysis
                    </button>

                    {video?.name && (
                        <div style={{ marginTop: 12 }}>
                            <video
                                controls
                                src={`/videos/${video.name}`}
                                className={styles.video}
                            />
                        </div>
                    )}
                </div>
            )}

            {verdict && (
                <div className={styles.verdictBox}>
                    <h2>AI Verdict</h2>
                    <pre className={styles.verdictPre}>{verdict}</pre>
                </div>
            )}
        </div>
    );
}
