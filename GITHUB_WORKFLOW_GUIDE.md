# 📋 GUIDA GITHUB WORKFLOW - CGSRef
## Regole Obbligatorie per Tutti gli Agent

---

## 🚨 REGOLE FONDAMENTALI (DA NON VIOLARE MAI)

### ❌ **COSA NON FARE MAI:**
1. **MAI modificare direttamente il branch `main`**
2. **MAI fare push su main senza aver testato**
3. **MAI unire branch che non funzionano**
4. **MAI perdere il lavoro dell'utente**
5. **MAI sovrascrivere file senza backup**

### ✅ **COSA FARE SEMPRE:**
1. **SEMPRE creare un branch per ogni modifica**
2. **SEMPRE testare in locale prima di unire**
3. **SEMPRE fare commit descrittivi**
4. **SEMPRE verificare che l'applicazione funzioni**
5. **SEMPRE fare backup del lavoro**

---

## 🔄 WORKFLOW STANDARD (SEGUIRE SEMPRE)

### **FASE 1: PREPARAZIONE**
```bash
# 1. Vai nella directory del progetto
cd "/Users/davidescantamburlo/Desktop/CGSRef copy"

# 2. Assicurati di essere su main aggiornato
git checkout main
git pull origin main

# 3. Verifica lo stato
git status
```

### **FASE 2: CREAZIONE BRANCH DI LAVORO**
```bash
# 4. Crea branch con nome descrittivo
git checkout -b [nome-descrittivo]

# Esempi di nomi validi:
# - nuovi-modelli-llm
# - workflow-video
# - integrazione-api-video
# - fix-bug-generazione
# - migliorie-frontend
```

### **FASE 3: SVILUPPO**
```bash
# 5. Lavora sui file necessari
# 6. Testa SEMPRE in locale:
#    - Avvia backend: python start_backend.py
#    - Avvia frontend: cd web/react-app && npm start
#    - Verifica che tutto funzioni

# 7. Salva il progresso frequentemente
git add .
git commit -m "Descrizione chiara di cosa è stato fatto"
```

### **FASE 4: BACKUP E SICUREZZA**
```bash
# 8. Backup del branch di lavoro
git push -u origin [nome-branch]
```

### **FASE 5: INTEGRAZIONE (SOLO SE TUTTO FUNZIONA)**
```bash
# 9. Torna a main
git checkout main

# 10. Unisci le modifiche
git merge [nome-branch]

# 11. Carica su entrambi i repository
git push origin main
git push fylleai main

# 12. Cleanup (opzionale)
git branch -d [nome-branch]
```

---

## 📝 CONVENZIONI PER COMMIT MESSAGES

### **Formato Obbligatorio:**
```
[tipo]: [descrizione breve]

[descrizione dettagliata se necessaria]
```

### **Tipi Validi:**
- `feat`: Nuova funzionalità
- `fix`: Correzione bug
- `docs`: Documentazione
- `style`: Formattazione
- `refactor`: Refactoring
- `test`: Test
- `chore`: Manutenzione

### **Esempi Corretti:**
```bash
git commit -m "feat: aggiunti modelli GPT-4 e Claude-3

- Configurazione provider in providers.py
- Aggiornamento frontend per selezione modelli
- Test di integrazione completati"

git commit -m "fix: risolto timeout generazione contenuti"

git commit -m "feat: nuovo workflow per video content"
```

---

## 🛠️ COMANDI ESSENZIALI

### **Navigazione:**
```bash
git branch                    # Vedi tutti i branch
git branch -a                 # Vedi branch locali e remoti
git status                    # Stato attuale
git log --oneline -5          # Ultimi 5 commit
```

### **Gestione Branch:**
```bash
git checkout [nome-branch]    # Cambia branch
git checkout -b [nome]        # Crea e cambia branch
git branch -d [nome]          # Elimina branch locale
```

### **Salvataggio:**
```bash
git add .                     # Aggiungi tutti i file
git add [file-specifico]      # Aggiungi file specifico
git commit -m "messaggio"     # Commit con messaggio
git push origin [branch]      # Push su GitHub
```

### **Sincronizzazione:**
```bash
git pull origin main          # Aggiorna da GitHub
git fetch --all              # Scarica tutti i branch
git merge [branch]            # Unisci branch
```

---

## 🚨 PROCEDURE DI EMERGENZA

### **Se Qualcosa Va Storto:**
```bash
# 1. STOP - Non fare altri comandi
# 2. Torna alla versione sicura
git checkout main

# 3. Verifica che main funzioni
python start_backend.py
# Se funziona, sei al sicuro

# 4. Se hai perso lavoro, recupera dal branch
git checkout [nome-branch-lavoro]
git log  # Vedi i commit salvati
```

### **Se l'Applicazione Non Funziona:**
```bash
# 1. Torna a main
git checkout main

# 2. Verifica che main funzioni
# 3. Se main non funziona, ripristina dall'ultimo commit funzionante
git reset --hard HEAD~1

# 4. Se ancora non funziona, scarica da GitHub
git fetch origin
git reset --hard origin/main
```

### **Se Hai Fatto Modifiche su Main per Errore:**
```bash
# 1. Crea branch di backup
git checkout -b backup-modifiche

# 2. Torna a main pulito
git checkout main
git reset --hard origin/main

# 3. Riapplica modifiche sul branch corretto
git checkout backup-modifiche
# Continua il lavoro qui
```

---

## 📋 CHECKLIST PRE-COMMIT

Prima di ogni commit, verifica:
- [ ] L'applicazione si avvia senza errori
- [ ] Backend risponde su http://localhost:8001
- [ ] Frontend si carica su http://localhost:3000
- [ ] Le nuove funzionalità funzionano
- [ ] Non ci sono errori nella console
- [ ] Il commit message è descrittivo

---

## 📋 CHECKLIST PRE-MERGE

Prima di unire a main, verifica:
- [ ] Tutti i test passano
- [ ] L'applicazione funziona completamente
- [ ] Non ci sono conflitti
- [ ] Il branch è aggiornato con main
- [ ] Hai fatto backup del branch

---

## 🎯 ESEMPI PRATICI

### **Esempio 1: Aggiungere Nuovi Modelli LLM**
```bash
git checkout main
git pull origin main
git checkout -b nuovi-modelli-llm

# Modifica core/infrastructure/config/providers.py
# Modifica web/react-app/src/components/ModelSelector.tsx
# Testa l'applicazione

git add .
git commit -m "feat: aggiunti modelli GPT-4 Turbo e Claude-3 Opus"
git push -u origin nuovi-modelli-llm

# Se tutto funziona:
git checkout main
git merge nuovi-modelli-llm
git push origin main
git push fylleai main
```

### **Esempio 2: Nuovo Workflow**
```bash
git checkout main
git pull origin main
git checkout -b workflow-video-content

# Crea core/infrastructure/workflows/handlers/video_handler.py
# Crea core/infrastructure/workflows/templates/video.json
# Aggiorna registry.py
# Testa il workflow

git add .
git commit -m "feat: nuovo workflow per generazione contenuti video"
git push -u origin workflow-video-content

# Se tutto funziona:
git checkout main
git merge workflow-video-content
git push origin main
git push fylleai main
```

---

## 📞 QUANDO CHIEDERE AIUTO

Chiedi sempre conferma all'utente prima di:
- Unire branch a main
- Eliminare branch
- Fare reset o modifiche irreversibili
- Caricare su GitHub

---

## 🔗 REPOSITORY CONFIGURATI

- **Principale:** git@github.com:FylleAI/cgsref.git (fylleai)
- **Backup:** git@github.com:MutenAI/cgsref.git (origin)

**SEMPRE caricare su entrambi dopo merge a main**
