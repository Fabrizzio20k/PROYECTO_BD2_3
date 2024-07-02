interface MessageProps {
    message: string;
    type: "error" | "success" | "info" | "warning" | "default";
}


export default function Message({ message, type }: MessageProps) {
    return (
        <div className={`bg-black ${type === "error" ? "text-red-500" :
            type === "success" ? "text-green-500" :
                type === "info" ? "text-blue-500" :
                    type === "warning" ? "text-yellow-500" :
                        "text-white"
            } font-mono p-4 rounded-lg shadow-lg mx-auto my-8 h-fit w-full`}>
            <p className="whitespace-pre-wrap">
                &gt; {message}
            </p>
        </div>
    );
}