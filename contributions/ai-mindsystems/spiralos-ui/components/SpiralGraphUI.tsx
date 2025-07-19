"use client";

import { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import { Card, CardContent } from "@/components/ui/card";

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

  useEffect(() => {
    setGraphData({
      nodes: [
        { id: "1", name: "JanusGraph", group: 1 },
        { id: "2", name: "Apollo Gateway", group: 2 },
        { id: "3", name: "UI Client", group: 3 },
      ],
      links: [
        { source: "1", target: "2" },
        { source: "2", target: "3" },
      ],
    });
  }, []);

  return (
    <Card className="p-4">
      <CardContent>
        <h2 className="text-xl font-semibold mb-4">Spiral Graph Visualization</h2>
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
