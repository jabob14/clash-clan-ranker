fetch('output/clan_data.json')
  .then(response => response.json())
  .then(data => {
    const clanInfo = data.clanInfo;
    
    document.getElementById("clan-badge").src = clanInfo.badge;
    document.getElementById("clan-name").textContent = clanInfo.name;
    const descriptionElement = document.getElementById("clan-description");
    const url = "https://docs.google.com/document/d/e/2PACX-1vR_V7CAp-Ay7loZoJUCGJmnhKkIVpiCuCCwFKg_1mtCWyi0oAHF79ScKXb1p1Wmxhm1-rlZS_QHUBlG/pub";
    descriptionElement.innerHTML = `Ranking sysytem för clanen COC BOYS <br> För mer info: <a href="${url}" target="_blank">${url}</a>`;
    document.getElementById("clan-level").textContent = `Level: ${clanInfo.level}`;
    document.getElementById("clan-members").textContent = `Members: ${clanInfo.members}`;

    const updatedDate = new Date(data.lastUpdated);
    document.getElementById("last-updated").textContent = `Updated: ${timeSince(updatedDate)} ago`;

    const membersContainer = document.getElementById("members");
    let rank = 1;

    const rankColors = {
      1: "#f8d65a",
      2: "#d1e0e9",
      3: "#e8b13f"
    };

    const headerRow = document.createElement("div");
    headerRow.className = "row header";
    headerRow.innerHTML = `
      <div class="rank">#</div>
      <div class="name">Name</div>
      <div class="donations">Donations</div>
      <div class="capital">Capital Hits</div>
      <div class="games">Clan Games</div>
      <div class="stars">CWL Stars</div>
      <div class="score">Total Score</div>`;
    membersContainer.appendChild(headerRow);

    for (const memberId in data.memberInfo) {
      const member = data.memberInfo[memberId];
      const row = document.createElement("div");
      row.className = "row";

      if (rankColors[rank]) {
        row.style.backgroundColor = rankColors[rank];
      }

      row.innerHTML = `
        <div class="rank">${rank}</div>
        <div class="name">${member.name}</div>
        <div class="donations">${member.donations}</div>
        <div class="capital">${member.capitalAttacks}</div>
        <div class="games">${member.clanGamesScore}</div>
        <div class="stars">${member.clanWarLeagueStars}</div>
        <div class="score">${member.totalScore}</div>
      `;
      membersContainer.appendChild(row);
      rank++;
    }
  })
  .catch(error => {
    console.error("Failed to load member data:", error);
  });

function timeSince(date) {
  const seconds = Math.floor((new Date() - date) / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  if (days > 0) return `${days} day${days !== 1 ? 's' : ''}`;
  if (hours > 0) return `${hours} hour${hours !== 1 ? 's' : ''}`;
  if (minutes > 0) return `${minutes} minute${minutes !== 1 ? 's' : ''}`;
  return `${seconds} second${seconds !== 1 ? 's' : ''}`;
}
