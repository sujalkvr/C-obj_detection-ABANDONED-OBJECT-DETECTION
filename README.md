# 🎥 Abandoned Object Detection using OpenCV

This project detects **abandoned or unattended objects** in surveillance video using Python and OpenCV. It identifies moving objects and flags them as "suspicious" if they remain static for an extended period.

---

## ⚙️ Dependencies

Install required libraries using:

```bash
pip install -r requirements.txt
Required Python packages:

opencv-python

numpy

🚀 How to Run
Make sure the input video and first reference frame (FrameNo0.png) are in the project directory.

Run the script:

bash
Copy
Edit
python main.py
Press q to stop the video processing window.

🧠 How It Works
The system uses the first video frame as a background reference.

It continuously compares each new frame to detect moving objects.

If an object stays in the same position for a prolonged period, it is flagged as a suspicious/abandoned object.

Such objects are highlighted with a red box and label.

📌 Features
Simple motion and contour-based detection

Custom object tracking without external libraries

Detects stationary objects after a defined threshold

Visual alerts on detected suspicious items

✅ Example Use Cases
Surveillance camera monitoring

Bag/package detection in public spaces

Security automation systems
