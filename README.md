# TechChallenge_5IADT_Fase2

Projeto de faculdade com foco em otimização de rotas utilizando Algoritmos Genéticos.

## 📌 Descrição

O objetivo deste projeto é simular um sistema de entregas que otimiza rotas de forma inteligente. Utilizamos um algoritmo genético que leva em conta a distância entre os pontos e o peso de tráfego de cada região, simulando áreas com maior ou menor trânsito.

## 🚀 Tecnologias

- Python 3
- Pygame
- Algoritmo Genético (customizado)
- Programação orientada a objetos

## 🔍 Como funciona

- São gerados 20 pontos de entrega com coordenadas e tráfego aleatórios.
- A cada geração, o algoritmo tenta melhorar a rota de entrega.
- A melhor rota é desenhada visualmente em uma janela Pygame.
- Ao final, são impressas:
  - A melhor rota encontrada
  - O tempo total estimado
  - O tempo entre cada par de pontos consecutivos

## 📊 Visualização

- A interface gráfica mostra:
  - A rota otimizada conectando todos os pontos
  - Gráfico de evolução do tempo ao longo das gerações
  - Identificadores dos pontos
  - Tempo total da melhor solução atual

## ▶️ Execução

1. Instale o Python 3.
2. Instale a dependência:

   ```bash
   pip install pygame
