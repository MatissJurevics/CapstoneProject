/*
Note: This is just for a proof of concept and LIKELY CANNOT HANDLE MULTIPLE STREAMS AT ONCE.
In order to handle multiple streams, use websockets
*/

import WebSocket from 'ws';
import fs from 'fs';
import path from 'path';

const PORT = 8080;
const wss = new WebSocket.Server({ port: PORT });

console.log(`Server started on port ${PORT}`);

if (!fs.existsSync('uploads')) {
    fs.mkdirSync('uploads');
}

wss.on('connection', (ws) => {
    console.log('Client connected');

    const outputPath = path.join(__dirname, 'uploads', `video-${Date.now()}.webm`);
    const writeStream = fs.createWriteStream(outputPath);

    ws.on('message', (data) => {
        // Write the incoming video chunks to a file
        writeStream.write(data);
    });

    ws.on('close', () => {
        console.log('Client disconnected');
        writeStream.end(); // Ensure the file is finalized
    });

    ws.on('error', (err) => {
        console.error('WebSocket error:', err);
        writeStream.end();
    });
});