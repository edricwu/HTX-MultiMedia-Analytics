import { render, fireEvent, screen } from "@testing-library/react";
import VideosPage from "../src/pages/videos";

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () =>
      Promise.resolve([
        {
          id: 1,
          filename: "video_01.mp4",
          summary: "Found 3 cars",
          created_at: "2025-11-20",
          detections: [
            { frame_index: 0, frame_base64: "AAAA" },
            { frame_index: 1, frame_base64: "BBBB" },
          ],
        },
      ]),
  })
) as any;

test("video viewer shows frame selection buttons and switches frames", async () => {
  render(<VideosPage />);

  // Select video from the list — ROLE-based avoids duplicate match
  const videoButton = await screen.findByRole("button", { name: /video_01\.mp4/i });
  fireEvent.click(videoButton);

  // Frame buttons appear
  const frame0Btn = await screen.findByText(/frame 0/i);
  const frame1Btn = await screen.findByText(/frame 1/i);

  expect(frame0Btn).toBeInTheDocument();
  expect(frame1Btn).toBeInTheDocument();

  // Switch to frame 1
  fireEvent.click(frame1Btn);
  expect(frame1Btn).toHaveClass("bg-blue-500"); // selected styling

  // Frame image updates
  const img = screen.getByRole("img");
  expect(img.getAttribute("src")).toContain("BBBB");
});
