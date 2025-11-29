# Política de Seguretat 🔒

Ens prenem molt seriosament la seguretat del projecte **Actor Recognition App**.  
Aquest document explica com reportar vulnerabilitats i quines són les nostres pràctiques de seguretat.

---

## 📌 Versions suportades

Només les versions actives del projecte reben actualitzacions de seguretat.  
Es recomana sempre utilitzar l’última versió publicada.

---

## 🚨 Reportar vulnerabilitats

Si detectes una vulnerabilitat de seguretat:

1. **No obris una issue pública.**
2. Contacta directament amb els mantenidors del projecte mitjançant correu electrònic privat.
3. Proporciona:
   - Descripció clara de la vulnerabilitat
   - Passos per reproduir-la
   - Impacte potencial
   - Possible solució (si en tens alguna)

---

## ✅ Bones pràctiques

- Mantén les dependències actualitzades (`requirements.txt` i Docker images).
- No comparteixis claus API ni credencials en el repositori.
- Utilitza `.env` per gestionar secrets i afegeix-lo al `.gitignore`.
- Executa els workflows de CI per validar que tot funciona correctament.

---

## 📜 Responsabilitat

Els mantenidors del projecte revisaran els informes de seguretat amb prioritat.  
Ens comprometem a:
- Respondre en un termini raonable
- Avaluar la gravetat
- Publicar un *patch* o actualització quan sigui necessari

---

## 📄 Llicència

Aquest projecte es distribueix sota la [llicència MIT](LICENSE).  
En reportar vulnerabilitats, acceptes que la informació es tracti de manera confidencial fins que es publiqui una solució.
