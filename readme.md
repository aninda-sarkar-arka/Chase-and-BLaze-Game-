

```markdown
# Chase and Blaze

**Chase and Blaze** is a 3D car combat survival game built with Python and PyOpenGL. Drive, boost, and fire missiles while dodging enemy cars in a city arena. The game features AI chasers, power-ups, multiple levels, health and score systems, explosive effects, and a dynamic HUD for an action-packed gameplay experience.

---

## 🚗 Features

### 1. Player (Main Car)
- **Movement Controls:** Use Arrow keys or WASD for movement (forward, backward, left, right).
- **Speed Boost (Nitro):** Press Shift to temporarily double your speed.
- **Firing System:** Shoot bullets or missiles with the Space key.
- **Health System:** Limited health that decreases upon being hit by enemies or collisions.
- **Score System:** Earn points for hitting enemies and surviving longer.

### 2. Enemy Cars
- **Chasing AI:** Enemy cars intelligently follow and chase the player.
- **Random Spawns:** New enemies appear at fixed intervals.
- **Firing Ability:** Some enemies can shoot at the player.
- **Collision Damage:** Lose health if an enemy car crashes into you.

### 3. Arena / Environment
- **City Arena:** Rectangular city arena with walls to restrict movement.
- **Dynamic Elements:** Exploding barrels and destructible objects add excitement.

### 4. Gameplay Mechanics
- **Bullets & Collisions:** Projectiles destroy enemies on impact.
- **Power-Ups:**
  - **Health Packs:** Restore player health.
  - **Shield:** Grants temporary invulnerability.
- **Game Over:** Happens when health drops to zero.
- **Win Condition:** Survive for a fixed time or destroy a certain number of enemies.

### 5. Levels & Progression
- **Level 1: Easy Chase:** Few slow enemies. Goal: Survive for a few minutes.
- **Level 2: Intense Pursuit:** More frequent enemy spawns. Goal: Destroy 10 enemies.
- **Level 3: Chaos Mode:** More obstacles and enemies. Goal: Survive 3 minutes & destroy 15 enemies.

### 6. Camera & Views
- **Third-Person View:** Camera follows behind the player’s car.
- **First-Person View:** Optional driver’s perspective.

### 7. UI & Feedback
- **HUD Elements:** Health bar, ammo count, score, timer.
- **Pop-Up Messages:** E.g., “Enemy Destroyed!”, “Health Restored!”, “Game Over!”
- **Pause/Resume System:** Pause and resume gameplay at any time.
- **Restart Option:** Quick restart after Game Over.

### 8. Extra Features
- **Explosion Effects:** Visual effects when cars are destroyed.
- **High Score Saving:** Best scores saved for replay value.

---

## 🕹️ Controls

| Action          | Key(s)                |
|-----------------|----------------------|
| Move            | Arrow Keys / WASD    |
| Speed Boost     | Shift                |
| Fire            | Space                |
| Pause/Resume    | P (or custom key)    |
| Restart         | R (or custom key)    |
| Switch Camera   | C (if implemented)   |

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aninda-sarkar-arka/Chase-and-BLaze-Game-.git
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the game:**
   ```bash
   python main.py
   ```

---

## 🛠️ Technologies Used

- **Python**
- **PyOpenGL**
- (Add any other libraries you use)

---

## 📄 License

This project is licensed under the MIT License.  
Feel free to fork, modify, and contribute!

---

## 🙏 Acknowledgements

- Thanks to all open-source contributors and Python game development communities for inspiration and support.

---

```

You can copy and paste this markdown into your `readme.md` file. If you need any edits or want to add images/screenshots, let me know!
