// app/api/graphql/route.ts

import { createSchema, createYoga } from 'graphql-yoga'
import { graphData } from '@/app/api/graph/store'
import { NextRequest } from 'next/server'

// Step 1: Define a default token (can be overridden via env)
const VALID_TOKEN = process.env.SOS_TOKEN ?? "spiral-dev-token"

const typeDefs = /* GraphQL */ `
  type Node {
    id: ID!
    name: String!
    group: Int!
  }

  type Link {
    source: String!
    target: String!
  }

  input NodeInput {
    id: ID!
    name: String!
    group: Int!
  }

  input LinkInput {
    source: String!
    target: String!
  }

  type Query {
    nodes: [Node!]!
    links: [Link!]!
  }

  type Mutation {
    addNode(input: NodeInput!): Node!
    addLink(input: LinkInput!): Link!
  }
`

const resolvers = {
  Query: {
    nodes: () => graphData.nodes,
    links: () => graphData.links,
  },
  Mutation: {
    addNode: (_: any, { input }: any, context: any) => {
      if (!context.isAuthorized) {
        throw new Error("Unauthorized")
      }
      graphData.nodes.push(input)
      return input
    },
    addLink: (_: any, { input }: any, context: any) => {
      if (!context.isAuthorized) {
        throw new Error("Unauthorized")
      }
      graphData.links.push(input)
      return input
    }
  }
}

const { handleRequest } = createYoga({
  graphqlEndpoint: '/api/graphql',
  schema: createSchema({ typeDefs, resolvers }),
  fetchAPI: { Request, Response },
  context: async ({ request }) => {
    const token = request.headers.get("authorization")
    const isAuthorized = token === `Bearer ${VALID_TOKEN}`
    return { isAuthorized }
  }
})

export async function GET(req: Request) {
  return handleRequest(req, {})
}

export async function POST(req: Request) {
  return handleRequest(req, {})
}
