import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import TrackCard from '../components/TrackCard';

const mockTrack = {
  TrackId: 1,
  track_name: 'Back In Black',
  artist_name: 'AC/DC',
  album_title: 'Back In Black',
  genre_name: 'Rock',
  UnitPrice: 0.99
};

describe('TrackCard', () => {
  test('renderiza el nombre de la canción', () => {
    render(<TrackCard track={mockTrack} onAdd={jest.fn()} />);
    expect(screen.getByText('Back In Black')).toBeInTheDocument();
  });

  test('renderiza el artista', () => {
    render(<TrackCard track={mockTrack} onAdd={jest.fn()} />);
    expect(screen.getByText(/AC\/DC/)).toBeInTheDocument();
  });

  test('renderiza el precio', () => {
    render(<TrackCard track={mockTrack} onAdd={jest.fn()} />);
    expect(screen.getByText('$0.99')).toBeInTheDocument();
  });

  test('llama onAdd cuando se hace click en Agregar', () => {
    const mockOnAdd = jest.fn();
    render(<TrackCard track={mockTrack} onAdd={mockOnAdd} />);
    fireEvent.click(screen.getByText('+ Agregar'));
    expect(mockOnAdd).toHaveBeenCalledWith(mockTrack);
  });

  test('renderiza el género', () => {
    render(<TrackCard track={mockTrack} onAdd={jest.fn()} />);
    expect(screen.getByText(/Rock/)).toBeInTheDocument();
  });
});
