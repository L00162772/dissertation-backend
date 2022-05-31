import { render, screen } from '@testing-library/react';
import App from './App';
// setup file
import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });
test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/React User Tracking/i);
  expect(linkElement).toBeInTheDocument();
});
