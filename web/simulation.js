let currentDay = 1;
let simulationIndex = 0;
let simulationData = [];

window.onload = async function() {
    simulationData = JSON.parse(await eel.get_simulation_results()());
    console.log(simulationData)
    const orderedStates = [];
    for (let i = 0; i < simulationData.length - 1; i++) {  // -1 to exclude winners data
        if ('day' in simulationData[i]) {
            orderedStates.push({type: "day", data: simulationData[i]});
            if (simulationData[i + 1] && 'night' in simulationData[i + 1]) {
                orderedStates.push({type: "intermission", data: {deaths: simulationData[i + 1].deaths, leaderboard: simulationData[i].leaderboard}});
            }
        }
        if ('night' in simulationData[i]) {
            orderedStates.push({type: "night", data: simulationData[i]});
        }
    }
    orderedStates.push({type: "winners", data: simulationData[simulationData.length - 1]});
    
    updatePage(orderedStates[simulationIndex]);

    document.getElementById('next').addEventListener('click', function() {
        if (simulationIndex < orderedStates.length - 1) {
            if (orderedStates[simulationIndex].type === 'night') {
                currentDay += 1;
            }
            simulationIndex += 1;
            updatePage(orderedStates[simulationIndex]);
        }
    });

    document.getElementById('previous').addEventListener('click', function() {
        if (simulationIndex > 0) {
            if (orderedStates[simulationIndex].type === 'day') {
                currentDay -= 1;
            }
            simulationIndex -= 1;
            updatePage(orderedStates[simulationIndex]);
        }
    });

    document.getElementById('reset-button').addEventListener('click', function() {
        // Store the reset request in local storage
        localStorage.setItem('resetRequest', 'true');
    
        // Redirect to the player selection page
        window.location.href = 'start.html';
    });
};

function updatePage(state) {
    document.getElementById('next').style.display = 'block';
    const currentState = state.type;
    let data = state.data;

    // Clear previous leaderboard, deaths, events, and alive players
    var leaderboardTable = document.getElementById('day1-leaderboard');
    var deathsContainer = document.getElementById('deaths-day1');
    var eventsContainer = document.getElementById('day1-events');
    var alivePlayersContainer = document.getElementById('alive-players-day1');
    var winnersContainer = document.getElementById('winners');
    var finalLeaderboardTable = document.getElementById('final-leaderboard');
    leaderboardTable.innerHTML = '';
    deathsContainer.innerHTML = '';
    eventsContainer.innerHTML = '';
    alivePlayersContainer.innerHTML = '';
    winnersContainer.innerHTML = '';
    finalLeaderboardTable.innerHTML = '';
    if (simulationIndex === 0) {
        document.getElementById('previous').style.display = 'none';
    } else {
        document.getElementById('previous').style.display = 'block';
    }
    if (currentState === "winners") {
        document.getElementById('state-number').textContent = 'Winners';
        data.winners.forEach(function(winner) {
            var winnerParagraph = document.createElement('p');
            winnerParagraph.textContent = winner;
            winnersContainer.appendChild(winnerParagraph);
        });
        data.final_leaderboard.forEach(function(player) {
            var row = finalLeaderboardTable.insertRow();
            var cell1 = row.insertCell();
            var cell2 = row.insertCell();
            var cell3 = row.insertCell();
            var cell4 = row.insertCell();
            cell1.textContent = player[0]; // District
            cell2.textContent = player[1]; // Player
            cell3.textContent = player[2]; // Status
            cell4.textContent = player[3]; // Kills
        });
        document.getElementById('next').style.display = 'none';
        return;
    }

    document.getElementById('state-number').textContent = `${currentState.charAt(0).toUpperCase() + currentState.slice(1)} ${currentDay}`;

    if (currentState === "intermission") {
        if (data && data.deaths) {
            data.deaths.flat().forEach(function(death) {
                var deathParagraph = document.createElement('p');
                deathParagraph.textContent = death;
                deathsContainer.appendChild(deathParagraph);
            });
        } else {
            deathsContainer.innerHTML = 'No deaths.';
        }

        if (data && data.leaderboard) {
            data.leaderboard.forEach(function(player) {
                var row = leaderboardTable.insertRow();
                var cell1 = row.insertCell();
                var cell2 = row.insertCell();
                var cell3 = row.insertCell();
                var cell4 = row.insertCell();
                cell1.textContent = player[0]; // District
                cell2.textContent = player[1]; // Player
                cell3.textContent = player[2]; // Status
                cell4.textContent = player[3]; // Kills
            });
        }
    } else if (currentState === "day" || currentState === "night") {  // "day" or "night"
        if (data) {
            if (data.events) {
                let leaderboardKey = (data.final_leaderboard !== undefined) ? 'final_leaderboard' : 'leaderboard';
                
                var deadPlayers = data[leaderboardKey]?.filter(player => player[2].startsWith('Died on')).map(player => player[1]);
                console.log(deadPlayers)

                data.events.forEach(function(event) {
                    var eventParagraph = document.createElement('p');
                    var eventInvolvesDeath = false;
                    eventInvolvesDeath = deadPlayers?.some(player => {
                        let regex = new RegExp(`\\b${player}\\b`);
                        return regex.test(event);
                    });
                    console.log("Event:", event);
                    console.log("Event Involves Death:", eventInvolvesDeath);
                    if (eventInvolvesDeath) {
                        console.log("This event involves death for the following players:");
                        deadPlayers.forEach(function(player) {
                            let regex = new RegExp(`\\b${player}\\b`);
                            if (regex.test(event)) {
                                console.log("- Player:", player);
                            }
                        });
                        eventParagraph.innerHTML = '<strong>' + event + '</strong>';
                    } else {
                        eventParagraph.textContent = event;
                    }
                    eventsContainer.appendChild(eventParagraph);
                });
                
            }
            if (data.alive_players) {
                alivePlayersContainer.textContent = 'Players Alive: ' + data.alive_players.join(', ');
            }
        }
    }
}
