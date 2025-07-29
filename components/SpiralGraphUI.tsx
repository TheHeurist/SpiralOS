"use client"

import { useEffect, useState } from "react"
import { gql, useQuery, useMutation } from "@apollo/client"
import ForceGraph2D from "react-force-graph-2d"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

type NodeType = {
  id: string
  name: string
  group: number
}

type LinkType = {
  source: string
  target: string
}

type GraphData = {
  nodes: NodeType[]
  links: LinkType[]
}

const GET_GRAPH = gql`
  query {
    nodes {
      id
      name
      group
    }
    links {
      source
      target
    }
  }
`

const ADD_NODE = gql`
  mutation($input: NodeInput!) {
    addNode(input: $input) {
      id
      name
      group
    }
  }
`

const ADD_LINK = gql`
  mutation($input: LinkInput!) {
    addLink(input: $input) {
      source
      target
    }
  }
`

export default function SpiralGraphUI() {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] })
  const [useGraphQL, setUseGraphQL] = useState(false)

  const { data: gqlData, loading: gqlLoading, error: gqlError } = useQuery(GET_GRAPH)

  const [addNode] = useMutation(ADD_NODE, {
    refetchQueries: [{ query: GET_GRAPH }],
  })

  const [addLink] = useMutation(ADD_LINK, {
    refetchQueries: [{ query: GET_GRAPH }],
  })

  const fetchGraph = async () => {
    try {
      const res = await fetch("/spiralos/api/graph")
      if (res.ok) {
        const data: GraphData = await res.json()
        setGraphData(data)
      } else {
        console.error("Failed to fetch graph data")
      }
    } catch (error) {
      console.error("Error fetching graph data:", error)
    }
  }

  useEffect(() => {
    fetchGraph()
  }, [])

  const activeGraphData: GraphData =
    useGraphQL && gqlData
      ? JSON.parse(JSON.stringify({ nodes: gqlData.nodes, links: gqlData.links }))
      : graphData

  return (
    <Card className="p-4">
      <CardContent>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Spiral Graph Visualization</h2>
          <div className="flex gap-2">
            {!useGraphQL && (
              <Button onClick={fetchGraph}>Refresh REST</Button>
            )}
            <Button onClick={() => setUseGraphQL(!useGraphQL)}>
              Use {useGraphQL ? "REST" : "GraphQL"}
            </Button>
            {useGraphQL && (
              <>
                <Button
                  onClick={() => {
                    const id = `node-${Date.now()}`
                    addNode({
                      variables: {
                        input: {
                          id,
                          name: `Node ${id.slice(-4)}`,
                          group: 5,
                        },
                      },
                    })
                  }}
                >
                  ➕ Add Node
                </Button>
                <Button
                  onClick={() => {
                    if (!gqlData?.nodes?.length) return
                    const last = gqlData.nodes[gqlData.nodes.length - 1]
                    addLink({
                      variables: {
                        input: {
                          source: last.id,
                          target: "1",
                        },
                      },
                    })
                  }}
                >
                  🔗 Link to JanusGraph
                </Button>
              </>
            )}
          </div>
        </div>

        <div style={{ height: "600px" }}>
          <ForceGraph2D
            graphData={activeGraphData}
            nodeLabel="name"
            nodeAutoColorBy="group"
          />
        </div>

        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-2">Apollo GraphQL Debug</h3>
          {gqlLoading && (
            <p className="text-sm text-gray-500">Loading GraphQL data...</p>
          )}
          {gqlError && (
            <p className="text-sm text-red-600">
              GraphQL error: {gqlError.message}
            </p>
          )}
          {gqlData && (
            <pre className="text-xs bg-gray-100 p-2 rounded max-h-[300px] overflow-auto">
              {JSON.stringify(gqlData, null, 2)}
            </pre>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
