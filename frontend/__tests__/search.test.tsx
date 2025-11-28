import { render, fireEvent, screen } from "@testing-library/react";
import SearchPage from "../src/pages/search";

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () =>
      Promise.resolve([
        { id: 1, type: "video", filename: "video_01.mp4", score: 0.98 }
      ])
  })
) as any;

test("search returns a video result with filename + score", async () => {
  render(<SearchPage />);

  // Updated placeholder text
  fireEvent.change(
    screen.getByPlaceholderText(/search objects\/transcript\/media name/i),
    { target: { value: "car" } }
  );

  fireEvent.click(screen.getByRole("button", { name: /search/i }));

  // filename appears
  expect(await screen.findByText(/video_01\.mp4/i)).toBeInTheDocument();

  // type label is now uppercase VIDEO
  expect(screen.getByText(/^VIDEO$/i)).toBeInTheDocument();

  // score label uses "score", not "similarity"
  expect(screen.getByText(/score 0\.980/i)).toBeInTheDocument();
});
