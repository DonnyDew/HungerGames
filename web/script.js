document.getElementById('num-players').addEventListener('input', function(e) {
    var numPlayers = e.target.value;
    var createPlayerFieldsButton = document.getElementById('create-player-fields');
    var errorSpan = document.getElementById('num-players-error');

    if (numPlayers < 12 || numPlayers > 24 || numPlayers % 2 !== 0) {
        errorSpan.textContent = 'Number of players must be an even number between 12 and 24';
        createPlayerFieldsButton.disabled = true;
    } else {
        errorSpan.textContent = '';
        createPlayerFieldsButton.disabled = false;
    }
});

document.getElementById('create-player-fields').addEventListener('click', function(e) {
    e.preventDefault();

    // Get the number of players
    var numPlayers = document.getElementById('num-players').value;

    // Get the player form
    var playerForm = document.getElementById('player-form');

    // Remove any existing player input fields
    while (playerForm.firstChild) {
        playerForm.removeChild(playerForm.firstChild);
    }

    // Create the player input fields
    for (var i = 1; i <= numPlayers; i++) {
        if (i % 2 === 1) {
            var teamDiv = document.createElement('div');
            var teamHeader = document.createElement('h3');
            teamHeader.textContent = 'District ' + ((i + 1) / 2);
            teamDiv.appendChild(teamHeader);
            playerForm.appendChild(teamDiv);
        }
        // Create a div for the player input fields
        var playerDiv = document.createElement('div');

        // Create the name input field
        var nameInput = document.createElement('input');
        nameInput.type = 'text';
        nameInput.id = 'player-name-' + i;
        nameInput.name = 'player-name-' + i;
        nameInput.required = true;
        
        // Set the default value to "Player n"
        nameInput.value = 'Player ' + i;

        // Create the gender select field
        var genderSelect = document.createElement('select');
        genderSelect.id = 'player-gender-' + i;
        genderSelect.name = 'player-gender-' + i;

        // Create the gender options
        var maleOption = document.createElement('option');
        maleOption.value = 'male';
        maleOption.text = 'Male';
        var femaleOption = document.createElement('option');
        femaleOption.value = 'female';
        femaleOption.text = 'Female';

        // Add the options to the select
        genderSelect.add(maleOption);
        genderSelect.add(femaleOption);

        // Set the default gender based on the player number
        if (i % 2 === 0) {
            genderSelect.value = 'female';
        } else {
            genderSelect.value = 'male';
        }

        var errorSpan = document.createElement('span');
        errorSpan.id = 'player-error-' + i;
        errorSpan.style.color = 'red';
        errorSpan.style.display = 'none';
        
        // Add the input fields to the div
        playerDiv.appendChild(nameInput);
        playerDiv.appendChild(genderSelect);
        playerDiv.appendChild(errorSpan);
        teamDiv.appendChild(playerDiv);

        nameInput.addEventListener('input', checkPlayerNames);

        // Add the div to the form
        playerForm.appendChild(playerDiv);
    }

    // Show the player form and the "Start Simulation" button
    playerForm.style.display = 'block';
    document.getElementById('start-simulation').style.display = 'block';
    console.log("create-player-fields finished");
});

function checkPlayerNames() {
    var playerNames = [...document.querySelectorAll('input[name^="player-name"]')].map(input => input.value.trim());
    var startSimulationButton = document.getElementById('start-simulation');
    var isValid = true;
    
    for (var i = 0; i < playerNames.length; i++) {
        var errorSpan = document.getElementById('player-error-' + (i + 1));
        var name = playerNames[i];
        
        if (name === '') {
            errorSpan.textContent = 'Name cannot be empty';
            errorSpan.style.display = 'inline';
            isValid = false;
        } else if (/[^a-zA-Z0-9\s]/.test(name)) {
            errorSpan.textContent = 'Special characters are not allowed';
            errorSpan.style.display = 'inline';
            isValid = false;
        } else if (playerNames.indexOf(name) !== playerNames.lastIndexOf(name)) {
            errorSpan.textContent = 'Duplicate name';
            errorSpan.style.display = 'inline';
            isValid = false;
        } else {
            errorSpan.style.display = 'none';
        }
    }
    
    if (isValid) {
        startSimulationButton.style.opacity = '1';
        startSimulationButton.disabled = false;
    } else {
        startSimulationButton.style.opacity = '0.5';
        startSimulationButton.disabled = true;
    }
}

document.getElementById('player-form').addEventListener('submit', async function(e) {
    console.log("player-form submitted");
    e.preventDefault();
    

    // Collect player names and genders and pass them to Python
    var playerNames = [...document.querySelectorAll('input[name^="player-name"]')].map(input => input.value);
    var playerGenders = [...document.querySelectorAll('select[name^="player-gender"]')].map(select => select.value);

    console.log("Player names:", playerNames);
    console.log("Player genders:", playerGenders);

    eel.create_players_and_teams(playerNames, playerGenders)(() => console.log('Players and teams created'));
});

document.getElementById('start-simulation').addEventListener('click', function(e) {
    console.log("start-simulation clicked");
    e.preventDefault();
    
    // Collect player names and genders and pass them to Python
    var playerNames = [...document.querySelectorAll('input[name^="player-name"]')].map(input => input.value);
    var playerGenders = [...document.querySelectorAll('select[name^="player-gender"]')].map(select => select.value);

    console.log("Player names:", playerNames);
    console.log("Player genders:", playerGenders);

    eel.create_players_and_teams(playerNames, playerGenders)(() => {
        console.log('Players and teams created');

        console.log("Start Simulation button clicked");
        eel.start_simulation()(simulation => {
            

            // Redirect to the simulation.html page
            go_to_simulation_page();
        });
    });
});

window.onload = function() {
    // Check for a reset request in local storage
    if (localStorage.getItem('resetRequest') === 'true') {
        // Reset the simulation
        if (typeof resetSimulation === 'function') {
            resetSimulation();
        }

        // Remove the reset request from local storage
        localStorage.removeItem('resetRequest');
    }
};




function go_to_simulation_page() {
    window.location.href = 'simulation.html';
}

eel.expose(go_to_simulation_page);



