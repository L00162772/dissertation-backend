import React from 'react';
import { shallow } from 'enzyme';
import {render, screen, fireEvent, cleanup} from '@testing-library/react';
import Read from './read';
import {BrowserRouter as Router} from 'react-router-dom';
import axios from 'axios'
jest.mock('axios');

afterEach(cleanup);
afterEach(() => {
    axios.get.mockClear();
  });

  function mockGetDataCallNoData() {
    axios.get.mockResolvedValueOnce({
      data: {}
    });
  }
  function mockGetDataCall1Result() {
    axios.get.mockResolvedValueOnce({
      data: {
        results: [
          {
            id: 1,
            firstName: 'First Name',
            lastName: 'Last Name',
            checkbox: 'Checked'
          },
        ]
      }
    });
  }
  
describe('<Read /> with no props', () => {
  let useEffect;
  const mockUseEffect = () => {
    useEffect.mockImplementationOnce(f => f());
  };
  beforeEach(() => {
    /* mocking useEffect */
    useEffect = jest.spyOn(React, "useEffect");
    mockUseEffect(); // 2 times
    mockUseEffect(); //
  });
  const container = shallow(<Router><Read /></Router>);

  it('should match the snapshot', () => {
    expect(container.html()).toMatchSnapshot();
  });
  
  it('should not load any content', () => {
    render(<Router><Read /></Router>);

    mockGetDataCall1Result()
    //const button = screen.getByTestId('update')
 


    //fireEvent.click(button)
  });
});