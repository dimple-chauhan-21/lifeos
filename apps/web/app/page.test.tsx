import { render, screen } from "@testing-library/react";
import { expect, test } from "vitest";

import HomePage from "./page";

test("renders the LifeOS placeholder", () => {
  render(<HomePage />);

  expect(screen.getByText("LifeOS")).toBeInTheDocument();
});
