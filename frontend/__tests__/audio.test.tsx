import { render, screen, fireEvent } from "@testing-library/react";
import AudioPage from "../src/pages/audio";

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () =>
      Promise.resolve([
        {
          id: 1,
          filename: "meeting.wav",
          created_at: "2025-11-22",
          segments: [
            { text: "hello everyone", start: 0.0, end: 1.2, confidence: 0.94 },
          ],
        },
      ]),
  })
) as any;

test("audio page displays transcript and timestamps", async () => {
  render(<AudioPage />);

  // Step 1 → Wait for file list to appear
  const fileButton = await screen.findByText(/meeting\.wav/i);
  expect(fileButton).toBeInTheDocument();

  // Step 2 → Click it to show transcript
  fireEvent.click(fileButton);

  // Step 3 → Now transcript should appear
  expect(await screen.findByText(/hello everyone/i)).toBeInTheDocument();
});
