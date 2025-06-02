import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import CameraViewer from "./components/CameraViewer";
import { getFaces } from "./api";

function App() {
  const [activeTab, setActiveTab] = useState("all");
  const [references, setReferences] = useState([]);
  const [results, setResults] = useState(null);

  const handleComplete = (data) => {
    setResults(data);
  };

  const loadAllFaces = async () => {
    const faces = await getFaces();
    setReferences(faces);
  };

  const showAllFaces = () => {
    setActiveTab("all");
    loadAllFaces();
  };

  return (
    <div className="p-4">
      {/* Tab Bar */}
      <nav className="flex space-x-4 border-b pb-2 mb-4">
        <button
          className={`px-4 py-2 ${
            activeTab === "all"
              ? "border-b-2 border-indigo-600 font-semibold"
              : "text-gray-600"
          }`}
          onClick={showAllFaces}
        >
          All Faces
        </button>

        <button
          className={`px-4 py-2 ${
            activeTab === "add"
              ? "border-b-2 border-indigo-600 font-semibold"
              : "text-gray-600"
          }`}
          onClick={() => {
            setActiveTab("add");
            setResults(null);
          }}
        >
          Add Person
        </button>

        <button
          className={`px-4 py-2 ${
            activeTab === "identify"
              ? "border-b-2 border-indigo-600 font-semibold"
              : "text-gray-600"
          }`}
          onClick={() => {
            setActiveTab("identify");
            setResults(null);
          }}
        >
          Identify
        </button>

        <button
          className={`px-4 py-2 ${
            activeTab === "camera"
              ? "border-b-2 border-indigo-600 font-semibold"
              : "text-gray-600"
          }`}
          onClick={() => {
            setActiveTab("camera");
            setResults(null);
          }}
        >
          Camera
        </button>
      </nav>

      {/* Tab Contents */}
      {activeTab === "all" && (
        <div>
          {references.length === 0 ? (
            <p className="text-gray-500">
              No faces yet. Click “All Faces” to load.
            </p>
          ) : (
            <div className="grid grid-cols-3 gap-4">
              {references.map((face) => (
                <div
                  key={face.image_url}
                  className="border p-2 text-center rounded"
                >
                  <img
                    src={`http://localhost:8000${face.image_url}`}
                    alt={face.name}
                    className="w-24 h-24 object-cover mx-auto rounded"
                  />
                  <p className="mt-2 font-medium">{face.name}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {(activeTab === "add" || activeTab === "identify") && (
        <div>
          <UploadForm
            mode={activeTab}
            onComplete={handleComplete}
          />

          {results && (
            <div className="mt-4 p-4 border rounded bg-gray-50">
              <pre className="whitespace-pre-wrap text-sm">
                {JSON.stringify(results, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}

      {activeTab === "camera" && <CameraViewer />}
    </div>
  );
}

export default App;
