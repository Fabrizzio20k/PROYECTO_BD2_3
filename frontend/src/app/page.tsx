"use client";

import { useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { useForm, Controller } from 'react-hook-form';
import Loader from "@/components/Loader";
import Message from "@/components/Message";
import Image from 'next/image';
import axios from 'axios';

const APIURL = 'http://127.0.0.1:8000';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [hovered, setHovered] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [fileError, setFileError] = useState<string | null>(null);
  const [message, setMessage] = useState<string>('Hello, world!');
  const [typeResults, setTypeResults] = useState<string>('default');

  const { handleSubmit, control, watch, formState: { errors } } = useForm({
    defaultValues: {
      typeSearch: '',
      value: '',
    },
  });

  const onDrop = (acceptedFiles: File[]) => {
    const selectedFile = acceptedFiles[0];
    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setFileError(null); // Clear any previous error when a new file is selected
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: { 'image/*': [] },
    maxFiles: 1,
  });

  const watchTypeSearch = watch('typeSearch');

  const onSubmit = (data: any) => {
    if (!file) {
      setFileError('Please select an image');
      return;
    }

    const formData = {
      photo: file,
      k: data.value,
      type_search: data.typeSearch,
    };

    console.log(formData);
  };

  useEffect(() => {
    const createIndex = async () => {
      try {
        setLoading(true);
        const { data } = await axios.post(`${APIURL}/create_index`);
        if (data.status_code === 200) {
          setMessage(data.message);
          setTypeResults('success');
        } else {
          setMessage(data.detail);
          setTypeResults('info');
        }
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    createIndex();
  }, []);

  return (
    <main className="bg-midnight-950 w-full h-screen flex justify-center">
      <Loader isActive={loading} />
      <section className="flex flex-col items-center max-w-[1920px] w-full px-10">
        <Message message={message} type={typeResults as "default" | "error" | "success" | "info" | "warning"} />
        <article className='w-full flex flex-col md:flex-row items-center'>
          <div className='w-full md:w-1/2'>
            <div className="flex justify-center space-x-6">
              <div
                {...getRootProps()}
                className={`relative border-2 border-dashed border-gray-300 bg-gray-800 rounded-lg p-6 text-center cursor-pointer w-full max-w-md aspect-square ${hovered ? 'opacity-75' : 'opacity-100'}`}
                onMouseEnter={() => setHovered(true)}
                onMouseLeave={() => setHovered(false)}
              >
                <input {...getInputProps()} />
                {preview ? (
                  <div className="absolute inset-0 w-full h-full">
                    <Image src={preview} alt="Preview" className="w-full h-full object-cover" width={256} height={256} />
                    {hovered && (
                      <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center text-white">
                        <p>Drop or click to upload an image</p>
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="text-gray-400">
                    {hovered ? 'Drop or click to upload an image' : 'Click to upload or drag and drop an image'}
                    <br />
                    Maximum file size 5 MB.
                  </p>
                )}
              </div>
            </div>
            {fileError && <p className="text-red-500 text-center mt-2">{fileError}</p>}
          </div>
          <div className='w-full md:w-1/2 flex flex-col h-full p-4'>
            <form onSubmit={handleSubmit(onSubmit)} className="w-full flex flex-col text-white">
              <label className="text-white mb-2">Modo de búsqueda</label>
              <Controller
                name="typeSearch"
                control={control}
                rules={{ required: 'Please select a search mode' }}
                render={({ field }) => (
                  <select {...field} className="mb-4 p-2 border-white border-2 rounded bg-blue-950">
                    <option value="">Select an option</option>
                    <option value="sequential">Sequential</option>
                    <option value="range">Range</option>
                    <option value="rtree">Rtree</option>
                    <option value="faiss">Faiss</option>
                  </select>
                )}
              />
              {errors.typeSearch && <p className="text-red-500">{errors.typeSearch.message}</p>}

              {watchTypeSearch && (
                <>
                  <label className="text-white mb-2">
                    {watchTypeSearch === 'range' ? 'Rango de búsqueda' : 'Objetos a recuperar (k)'}
                  </label>
                  <Controller
                    name="value"
                    control={control}
                    rules={{ required: 'Please enter a value' }}
                    render={({ field }) => (
                      <input
                        {...field}
                        type="number"
                        className="mb-4 p-2 border rounded border-white bg-blue-950"
                        step={watchTypeSearch === 'range' ? '0.01' : '1'}
                      />
                    )}
                  />
                  {errors.value && <p className="text-red-500">{errors.value.message}</p>}
                </>
              )}
              <button
                type="submit"
                className="mt-4 w-full bg-blue-900 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
              >
                Attach file
              </button>
            </form>
          </div>
        </article>
      </section>
    </main>
  );
}
