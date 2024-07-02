"use client";

import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import Loader from "@/components/Loader";
import Message from "@/components/Message";
import Image from 'next/image';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);

  const onDrop = (acceptedFiles: File[]) => {
    const selectedFile = acceptedFiles[0];
    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: { 'image/*': [] },
    maxFiles: 1,
  });

  const handleSubmit = () => {
    if (file) {
      console.log('File name:', file.name);
    } else {
      console.log('No file selected');
    }
  };

  return (
    <main className="bg-midnight-950 w-full h-screen flex">
      <Loader isActive={false} />
      <section className="flex flex-col items-center max-w-[1920px] w-full px-10">
        <Message message="Hello, world!" type="success" />
        <article>
          <div className="flex items-start space-x-6 mt-10">
            <div
              {...getRootProps()}
              className="border-2 border-dashed border-gray-300 bg-gray-800 rounded-lg p-6 text-center cursor-pointer"
            >
              <input {...getInputProps()} />
              {file ? (
                <p className="text-white">{file.name}</p>
              ) : (
                <p className="text-gray-400">
                  Click to upload or drag and drop an image<br />
                  Maximum file size 50 MB.
                </p>
              )}
            </div>
            {preview && (
              <div className="w-48 h-48 bg-gray-200 rounded-lg overflow-hidden">
                <Image src={preview} alt="Preview" className="w-full h-full object-cover" width={1920} height={1080} />
              </div>
            )}
          </div>
          <button
            onClick={handleSubmit}
            className="mt-4 w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600"
          >
            Attach file
          </button>
        </article>
      </section>
    </main>
  );
}
