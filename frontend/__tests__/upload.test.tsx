import { render, screen, fireEvent } from "@testing-library/react";
import UploadPage from "../src/pages/upload";

test("upload accepts both video and audio files", () => {
  render(<UploadPage />);

  const input = screen.getByTestId("upload-input") as HTMLInputElement;

  Object.defineProperty(input, "files", {
    value: [
      new File([""], "sample.mp4", { type: "video/mp4" }),
      new File([""], "sample.wav", { type: "audio/wav" })
    ]
  });

  fireEvent.change(input);
  expect(input.files?.length).toBe(2);
});
