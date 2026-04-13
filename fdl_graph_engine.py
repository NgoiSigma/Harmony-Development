fdl_graph_engine.py

""" FDL Graph Engine — модуль визуализации смысловых связей и логических потоков громады Основан на FDL-парадигме и логике СВЕТ """

import networkx as nx import matplotlib.pyplot as plt

class FDLGraphEngine: def init(self): self.graph = nx.DiGraph()

def add_node(self, node_id, label, type_='узел', resonance_level=1):
    self.graph.add_node(node_id, label=label, type=type_, resonance=resonance_level)

def add_edge(self, source_id, target_id, label=None, weight=1):
    self.graph.add_edge(source_id, target_id, label=label, weight=weight)

def visualize(self, title='FDL :: Смыслограф', layout='spring'):
    pos = nx.spring_layout(self.graph) if layout == 'spring' else nx.shell_layout(self.graph)
    labels = nx.get_node_attributes(self.graph, 'label')
    node_colors = ['#ffd700' if d['resonance'] > 1 else '#87ceeb' for n, d in self.graph.nodes(data=True)]
    
    nx.draw(self.graph, pos, with_labels=True, labels=labels, node_color=node_colors, node_size=700, font_size=9)
    edge_labels = nx.get_edge_attributes(self.graph, 'label')
    nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
    
    plt.title(title)
    plt.axis('off')
    plt.show()

def export_graph(self, filename='fdl_graph.gml'):
    nx.write_gml(self.graph, filename)

def reset(self):
    self.graph.clear()

Пример использования

if name == 'main': engine = FDLGraphEngine() engine.add_node('ZAMYSEL', 'Замысел', resonance_level=3) engine.add_node('FORMA', 'Форма') engine.add_node('POTOK', 'Поток') engine.add_edge('ZAMYSEL', 'FORMA', 'структурирует') engine.add_edge('FORMA', 'POTOK', 'направляет') engine.visualize()

______
<?xml version="1.0" encoding="UTF-8"?><svg width="300" height="300" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fff8dc"/>
      <stop offset="100%" stop-color="#ffd700" stop-opacity="0.2"/>
    </radialGradient>
  </defs>  <!-- Основа круга -->  <circle cx="150" cy="150" r="140" fill="url(#glow)" stroke="#8b0000" stroke-width="4" />  <!-- Центральный символ Tau -->  <text x="150" y="165" text-anchor="middle" font-size="96" font-family="Georgia, serif" fill="#4b0082">
    τ
  </text>  <!-- Орнаментальные кольца -->  <circle cx="150" cy="150" r="100" fill="none" stroke="#4b0082" stroke-dasharray="6,6" stroke-width="1.5" />
  <circle cx="150" cy="150" r="120" fill="none" stroke="#ffd700" stroke-width="1" />  <!-- Надпись SIGIL -->  <text x="150" y="280" text-anchor="middle" font-size="16" font-family="monospace" fill="#444">
    TAURUS · ΣIGIL · NOVEYA
  </text>
</svg>
