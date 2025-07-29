'use client'

import {
  ApolloClient,
  InMemoryCache,
  HttpLink,
  ApolloLink,
} from '@apollo/client'
import fetch from 'cross-fetch' // ✅ Required for Node.js and Jest environments

const authLink = new ApolloLink((operation, forward) => {
  operation.setContext(({ headers = {} }) => ({
    headers: {
      ...headers,
      authorization: 'Bearer spiral-dev-token',
    },
  }))
  return forward(operation)
})

const httpLink = new HttpLink({
  uri: '/api/graphql',
  fetch, // ✅ Inject fetch explicitly so it works in all environments
})

const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
})

export default client
