# ⚡ QUICK REFERENCE - Comandi Git Essenziali

## 🚀 INIZIO LAVORO (SEMPRE)
```bash
cd "/Users/davidescantamburlo/Desktop/CGSRef copy"
git checkout main
git pull origin main
git checkout -b [nome-descrittivo]
```

## 💾 SALVARE LAVORO
```bash
git add .
git commit -m "feat: descrizione di cosa hai fatto"
git push -u origin [nome-branch]
```

## ✅ COMPLETARE LAVORO (SOLO SE FUNZIONA)
```bash
# Testa prima che tutto funzioni!
python start_backend.py  # Deve partire senza errori
cd web/react-app && npm start  # Deve caricare senza errori

# Se tutto OK:
git checkout main
git merge [nome-branch]
git push origin main
git push fylleai main
```

## 🆘 EMERGENZA - TORNA AL SICURO
```bash
git checkout main
# Ora sei sulla versione che funziona sempre
```

## 📋 VERIFICA STATO
```bash
git branch          # Dove sono?
git status          # Cosa ho modificato?
git log --oneline -3  # Ultimi commit
```

## 🔄 PATTERN COMPLETO
```bash
# 1. PREPARA
git checkout main && git pull origin main

# 2. LAVORA
git checkout -b mia-modifica
# ... modifica file ...
# ... testa che funzioni ...

# 3. SALVA
git add . && git commit -m "feat: cosa ho fatto"
git push -u origin mia-modifica

# 4. INTEGRA (solo se tutto OK)
git checkout main
git merge mia-modifica
git push origin main && git push fylleai main
```

## 🎯 NOMI BRANCH ESEMPI
- `nuovi-modelli-llm`
- `workflow-video`
- `fix-bug-timeout`
- `migliorie-frontend`
- `integrazione-api-video`

## ⚠️ REGOLE D'ORO
1. **MAI lavorare su main direttamente**
2. **SEMPRE testare prima di merge**
3. **SEMPRE fare backup con push**
4. **UN branch = UNA cosa**

## 🔧 TEST RAPIDO FUNZIONAMENTO
```bash
# Backend (deve dire "Started server process")
python start_backend.py

# Frontend (deve aprire browser su localhost:3000)
cd web/react-app && npm start
```

## 📞 IN CASO DI DUBBI
1. Ferma tutto
2. `git checkout main`
3. Chiedi aiuto all'utente
4. Mostra questa guida
