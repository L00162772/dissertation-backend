import React from 'react';
import { shallow } from 'enzyme';
import {render, screen, fireEvent, cleanup} from '@testing-library/react';
import Update from './update';
import {BrowserRouter as Router} from 'react-router-dom';
import axios from 'axios'
jest.mock('axios');

afterEach(cleanup);
afterEach(() => {
    axios.put.mockClear();
  });

  function mockPutDataCall() {
    axios.put.mockResolvedValueOnce({
      data: {
        results: [
          {
            name: {
              first: "name 1"
            }
          },
          {
            name: {
              first: "name 2"
            }
          }
        ]
      }
    });
  }

describe('<Update /> with no props', () => {
  const container = shallow(<Router><Update /></Router>);

  it('should match the snapshot', () => {
    expect(container.html()).toMatchSnapshot();
  });
  
  // See https://testing-library.com/docs/react-testing-library/cheatsheet
  //https://testing-library.com/docs/example-input-event/
  it('should have firstName field', () => {
    render(<Router><Update /></Router>);
    const input = screen.getByTestId('firstName');
    expect(input).toBeInTheDocument()
    expect(input).toHaveAttribute('placeholder',  'First Name')
    expect(input).toHaveAttribute('type',  'text')
  });

  it('should accept changes in firstName field', () => {
    render(<Router><Update /></Router>);
    const input = screen.getByTestId('firstName');
    fireEvent.change(input, {target: {value: 'first name'}})
    expect(input.value).toBe('first name')
  });

  it('should have lastName field', () => {
    render(<Router><Update /></Router>);
    const input = screen.getByTestId('lastName');
    expect(input).toBeInTheDocument()
    expect(input).toHaveAttribute('placeholder',  'Last Name')
    expect(input).toHaveAttribute('type',  'text')
  });

  it('should accept changes in lastName field', () => {
    render(<Router><Update /></Router>);
    const input = screen.getByTestId('lastName')
    fireEvent.change(input, {target: {value: 'last name'}})
    expect(input.value).toBe('last name')
  });

  it('should have terms field', () => {
    render(<Router><Update /></Router>);
    const input = screen.getByTestId('terms')
    expect(input).toBeInTheDocument()
    const checkboxLabel = input.children[1]
    expect(checkboxLabel).toHaveTextContent("I agree to the Terms and Conditions")
  });

  it('should accept changes to terms checkbox', () => {
    render(<Router><Update /></Router>);
    const input= screen.getByTestId('terms') 

    const checkboxInput = input.children[0]
    fireEvent.click(checkboxInput)
    expect(input).toHaveAttribute('class',  'ui checked checkbox')

    fireEvent.click(checkboxInput)
    expect(input).toHaveAttribute('class',  'ui checkbox')
  });

  it('should have submit button', () => {
    render(<Router><Update /></Router>);
    const button = screen.getByTestId('update')
    expect(button).toBeInTheDocument()
    expect(button).toHaveAttribute('type',  'submit')
  });

  it('should trigger submit button', () => {
    render(<Router><Update /></Router>);
    const button = screen.getByTestId('update')

    mockPutDataCall();

    fireEvent.click(button)
  });
});