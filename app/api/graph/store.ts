export type NodeType = {
  id: string;
  name: string;
  group: number;
};

export type LinkType = {
  source: string;
  target: string;
};

export type GraphData = {
  nodes: NodeType[];
  links: LinkType[];
};

export const graphData: GraphData = {
  nodes: [
    { id: "1", name: "JanusGraph", group: 1 },
    { id: "2", name: "Apollo Gateway", group: 2 },
    { id: "3", name: "UI Client", group: 3 },
  ],
  links: [
    { source: "1", target: "2" },
    { source: "2", target: "3" },
  ],
};
