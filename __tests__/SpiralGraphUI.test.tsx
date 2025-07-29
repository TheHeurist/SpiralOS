import React from 'react'
import { render, screen } from '@testing-library/react'
import SpiralGraphUI from '@/components/SpiralGraphUI'
import { ApolloProvider } from '@apollo/client'
import client from '@/lib/apollo-client'

jest.mock('react-force-graph-2d', () => () => <div data-testid="mock-force-graph" />)

test('renders Spiral Graph header', () => {
  render(
    <ApolloProvider client={client}>
      <SpiralGraphUI />
    </ApolloProvider>
  )
  expect(screen.getByText(/Spiral Graph Visualization/i)).toBeInTheDocument()
  expect(screen.getByTestId('mock-force-graph')).toBeInTheDocument()
})
