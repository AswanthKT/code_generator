import { useState } from "react";
import { Button, Input } from "@/components/ui";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000"); // Update with backend URL

export default function ModelInstaller() {
  const [modelName, setModelName] = useState("");
  const [progress, setProgress] = useState([]);
  const [installing, setInstalling] = useState(false);

  const handleInstall = () => {
    if (!modelName) return;
    setInstalling(true);
    setProgress(["Generating installation commands..."]);
    socket.emit("install_model", modelName);
  };

  socket.on("progress", (message) => {
    setProgress((prev) => [...prev, message]);
    if (message.includes("Installation complete")) setInstalling(false);
  });

  return (
    <div className="flex flex-col items-center gap-4 p-6">
      <h1 className="text-2xl font-bold">AI Model Installer</h1>
      <Input
        value={modelName}
        onChange={(e) => setModelName(e.target.value)}
        placeholder="Enter model name"
        disabled={installing}
      />
      <Button onClick={handleInstall} disabled={installing}>
        Install
      </Button>
      <div className="w-full max-w-md mt-4 p-4 border rounded-lg">
        <h2 className="text-lg font-semibold">Installation Progress:</h2>
        <ul className="mt-2 text-sm">
          {progress.map((msg, idx) => (
            <li key={idx}>{msg}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
