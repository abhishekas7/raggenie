import { render, screen } from "@testing-library/react";
import Button from "./Button";

describe("Button component", () => {
  it("should render Button component correctly", () => {
    render(<Button>Click me</Button>);
    const buttonElement = screen.getByRole("button"); 
  });

  it("should render different button types and variants correctly", () => {
    render(<Button>Transparent Warning Button</Button>);
    const transparentButton = screen.getByRole("button", {  type: "transparent",variant:"danger"  });
    const solid = screen.getByRole("button", {  type: "solid",variant:"primary-secondary"});

  });


});
