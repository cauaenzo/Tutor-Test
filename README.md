# Tutor-Test
teste de tutor python
## Jogo de Herói e Inimigos

Este é um jogo simples desenvolvido com a biblioteca **pgzero (pgzrun)**, onde você controla um herói azul que deve eliminar inimigos vermelhos enquanto evita colisões com eles.

---

## Configurações Básicas

- Resolução da tela: 640x480 pixels.
- Tamanho do tile (bloco): 32x32 pixels.
- Taxa de quadros: 30 FPS.
- Paleta de cores:
  - Chão: marrom.
  - Herói: azul com animação de 2 frames.
  - Inimigos: vermelho com animação de 2 frames.
  - Tiros: amarelo.
  - Botões: tons de cinza.
  - Texto: branco.

---

## Classes do Jogo

- **AnimatedSprite**: Controla sprites animados, incluindo posição e animação de frames.
- **Hero**: Personagem controlado pelo jogador, com movimento e direção para disparos.
- **Enemy**: Inimigos que patrulham territórios limitados, mudando de direção ao atingir limites.
- **Bullet**: Tiros disparados pelo herói, que se movem até sair da tela ou atingir inimigos.
- **Button**: Botões interativos para o menu e tela de vitória, com reação a hover e clique.

---

## Funcionalidades Principais

- **Iniciar jogo**: Botão inicia o jogo, posicionando o herói no centro e gerando inimigos.
- **Movimentação**: Controle o herói com as setas do teclado.
- **Disparo**: Pressione espaço para atirar na última direção do herói.
- **Inimigos**: Cinco inimigos patrulham áreas fixas e podem ser eliminados.
- **Colisão**:
  - Contato do herói com inimigos retorna ao menu (game over).
  - Tiros eliminam inimigos e aumentam a pontuação.
- **Menu**: Contém botões para iniciar o jogo, ativar/desativar som e sair.
- **Som**: Música ambiente ativável no menu e durante o jogo.
- **Vitória**: Ao eliminar todos os inimigos, mensagem de vitória é exibida junto a botão para voltar ao menu.

---

## Controles

| Tecla / Ação | Função                         |
|--------------|-------------------------------|
| Setas        | Movimentar o herói            |
| Espaço       | Atirar na direção atual       |
| Esc          | Voltar ao menu ou sair da tela de vitória |
| Mouse        | Navegar e clicar nos botões   |

---

## Estrutura do Código

- O jogo funciona com um loop principal via `pgzrun.go()`.
- Funções chave:
  - `update()` — atualiza a lógica do jogo.
  - `draw()` — desenha todos os elementos na tela.
  - `on_key_down()` — gerencia eventos de teclado.
  - `on_mouse_move()` e `on_mouse_down()` — gerenciam interação com botões.
- Estados do jogo:
  - `menu`
  - `playing`
  - `won`
- Animações simples trocando entre dois tons para herói e inimigos.

---

## Música e Sons

- Música ambiente em loop no menu e no jogo.
- Botão para ativar ou pausar o som.
- Volume ajustado para 50%.
- Arquivo de música esperado: `music/robot_city.mp3`.

---

## Pontuação

- Cada inimigo eliminado soma 10 pontos.
- Placar exibido no canto superior esquerdo em todos os estados.

---
## Como rodar
`1` instale o projeto por .ZIP ou por GitBash
```gitbash
git clone https://github.com/cauaenzo/Tutor-Test
```
`2` criar um ambiente virtual(só se quiser)
```bash
python -m venv venv
```
`3` instalar as dependencias
```bash
pip install -r requirements.txt
```
`4` Executar o Projeto
```bash
python main.py
```
---
# Considerações
Sinceramente foi um desafio usar esse pgzrun, já fiz inumeros jogos usando pygame e definitivamente fazer usando somente 
o rect do pygame e o resto na mão é algo massante demais, e ainda mais em um arquivo só, complicado.
