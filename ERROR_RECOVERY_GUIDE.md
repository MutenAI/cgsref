# 🚨 GUIDA RECUPERO ERRORI - CGSRef

## ⚠️ PRINCIPIO BASE
**In caso di qualsiasi errore: FERMA TUTTO e torna a main**
```bash
git checkout main
```

---

## 🔥 ERRORI COMUNI E SOLUZIONI

### **1. "L'applicazione non si avvia più"**
```bash
# SOLUZIONE:
git checkout main
python start_backend.py  # Deve funzionare

# Se main non funziona:
git fetch origin
git reset --hard origin/main
```

### **2. "Ho modificato main per errore"**
```bash
# SOLUZIONE:
# 1. Salva le modifiche in un branch
git checkout -b salvataggio-modifiche

# 2. Ripristina main pulito
git checkout main
git reset --hard origin/main

# 3. Continua il lavoro sul branch salvataggio
git checkout salvataggio-modifiche
```

### **3. "Non riesco a fare merge"**
```bash
# SOLUZIONE:
# 1. Annulla il merge
git merge --abort

# 2. Torna al sicuro
git checkout main

# 3. Riprova più tardi o chiedi aiuto
```

### **4. "Ho perso il mio lavoro"**
```bash
# SOLUZIONE:
# 1. Controlla tutti i branch
git branch -a

# 2. Cerca nei commit recenti
git log --oneline --all -10

# 3. Se hai fatto push, recupera da GitHub
git fetch origin
git checkout origin/[nome-branch]
git checkout -b recupero-lavoro
```

### **5. "Conflitti durante merge"**
```bash
# SOLUZIONE:
# 1. Annulla il merge
git merge --abort

# 2. Torna a main
git checkout main

# 3. Chiedi aiuto all'utente
```

### **6. "Push rifiutato"**
```bash
# SOLUZIONE:
# 1. Aggiorna prima
git pull origin [branch-name]

# 2. Se ci sono conflitti, annulla
git merge --abort
git checkout main

# 3. Chiedi aiuto
```

---

## 🛡️ PROCEDURE DI SICUREZZA

### **Prima di Ogni Operazione Rischiosa:**
```bash
# 1. Verifica dove sei
git branch
git status

# 2. Se non sei su main, vai su main
git checkout main

# 3. Assicurati che main funzioni
python start_backend.py
# Deve partire senza errori
```

### **Backup Automatico:**
```bash
# Prima di modifiche importanti
git checkout -b backup-$(date +%Y%m%d-%H%M%S)
git checkout main
# Ora procedi con le modifiche
```

---

## 🔄 RESET COMPLETO (ULTIMA RISORSA)

### **Se Tutto è Rotto:**
```bash
# 1. Salva tutto quello che puoi
git stash push -m "Salvataggio emergenza"

# 2. Torna a main pulito
git checkout main
git fetch origin
git reset --hard origin/main

# 3. Verifica che funzioni
python start_backend.py

# 4. Se hai salvato qualcosa, recupera
git stash list
git stash pop  # Solo se necessario
```

---

## 📋 CHECKLIST RECUPERO

Quando qualcosa va storto:
- [ ] STOP - Non fare altri comandi
- [ ] `git checkout main`
- [ ] Testa che main funzioni
- [ ] Se main funziona, sei al sicuro
- [ ] Identifica il problema
- [ ] Applica la soluzione appropriata
- [ ] Testa di nuovo
- [ ] Se non risolvi, chiedi aiuto

---

## 🆘 COMANDI DI EMERGENZA

```bash
# Torna al sicuro
git checkout main

# Annulla merge in corso
git merge --abort

# Annulla rebase in corso
git rebase --abort

# Salva tutto temporaneamente
git stash push -m "Emergenza"

# Ripristina main da GitHub
git fetch origin
git reset --hard origin/main

# Vedi cosa è successo
git log --oneline -5
git reflog -5
```

---

## 📞 QUANDO CHIEDERE AIUTO

Chiedi SEMPRE aiuto se:
- Non capisci un messaggio di errore
- Hai paura di perdere lavoro
- Main non funziona più
- Vedi conflitti che non capisci
- Qualsiasi operazione sembra rischiosa

**MEGLIO CHIEDERE CHE ROMPERE!**

---

## 🎯 MESSAGGI DI ERRORE COMUNI

### **"fatal: not a git repository"**
```bash
# Sei nella cartella sbagliata
cd "/Users/davidescantamburlo/Desktop/CGSRef copy"
```

### **"error: pathspec 'branch' did not match"**
```bash
# Il branch non esiste
git branch -a  # Vedi tutti i branch
```

### **"error: Your local changes would be overwritten"**
```bash
# Hai modifiche non salvate
git stash push -m "Salvataggio temporaneo"
# Poi riprova il comando
```

### **"CONFLICT (content): Merge conflict"**
```bash
# Conflitti durante merge
git merge --abort  # Annulla tutto
git checkout main  # Torna al sicuro
```

---

## ✅ VERIFICA FINALE

Dopo ogni recupero:
```bash
# 1. Sei su main?
git branch

# 2. Main è aggiornato?
git status

# 3. L'app funziona?
python start_backend.py
cd web/react-app && npm start
```
