"use client";

import { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

type NodeType = {
  id: string;
  name: string;
  group: number;
};

type LinkType = {
  source: string;
  target: string;
};

type GraphData = {
  nodes: NodeType[];
  links: LinkType[];
};

export default function SpiralGraphUI() {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });

  const fetchGraph = async () => {
    try {
      const res = await fetch("/spiralos/api/graph");
      if (res.ok) {
        const data: GraphData = await res.json();
        setGraphData(data);
      } else {
        console.error("Failed to fetch graph data");
      }
    } catch (error) {
      console.error("Error fetching graph data:", error);
    }
  };

  useEffect(() => {
    fetchGraph();
  }, []);

  return (
    <Card className="p-4">
      <CardContent>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Spiral Graph Visualization</h2>
          <Button onClick={fetchGraph}>Refresh Graph</Button>
        </div>
        <div style={{ height: "600px" }}>
          <ForceGraph2D
            graphData={graphData}
            nodeLabel="name"
            nodeAutoColorBy="group"
          />
        </div>
      </CardContent>
    </Card>
  );
}
