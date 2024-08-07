exercise = 1;

function addSet(currentEx, currentSet){
    // TODO: Create a function that adds another set block to an exercise block
    // Create the integer of the next set
    nextSet = currentSet + 1;

    // Create the new HTML block with the new indicator
    document.getElementById('ex-'+ currentEx).insertAdjacentHTML("beforeend", '<div class="set" id="ex-'+ currentEx +'-set-' + nextSet + '">'
        + '<!-- Buttons -->'
        + '<h4 onclick="removeSet(' + currentEx + ', ' + nextSet + ')" class="remove-button">Remove set</h4>'
        + '<h3>Set ' + nextSet + '</h3>'
        + '<!-- Reps & Weights -->'
        + '<input type="text" name="ex-' + currentEx + '-set-' + nextSet + '-reps" placeholder="Reps">'
        + '<input type="text" name="ex-' + currentEx + '-set-' + nextSet + '-weight" placeholder="Weight">'
    )

    // Change the value of the add-set button
    button = document.getElementById('add-set-ex-' + currentEx)
    button.setAttribute("onclick", `addSet(${currentEx}, ${nextSet})`)
    console.log(button)
}

function addExercise() {
    // TODO: Create a new exercise block
    // Increase the exercise indicator
    exercise++;

    // Create the new super long HTML
    document.getElementById('routine').insertAdjacentHTML('beforeend', '<div class="exercise" id="ex-'+ exercise +'">'
        + '<!-- Buttons -->'
        + '<h4 onclick="removeExercise('+ exercise +')" class="remove-button">Remove exercise</h4>'
        + '<!-- Title -->'
        + '<input type="text" name="ex-name-'+ exercise +'" placeholder="Exercises name">'
        + '<h4 onclick="addSet('+ exercise +', 1)" id="add-set-ex-'+ exercise +'" class="add-button">Add set</h4>'
        + '<!-- Sets -->'
        + '<div class="set" id="ex-'+ exercise +'set-1">'
        + '<!-- Buttons -->'
        + '<h4 onclick="removeSet('+ exercise +', 1)" class="remove-button">Remove set</h4>'
        + '<h3>Set 1</h3>'
        + '<!-- Reps & Weights -->'
        + '<input type="text" name="ex-'+ exercise +'-set-1-reps" placeholder="Reps">'
        + '<input type="text" name="ex-'+ exercise +'-set-1-weight" placeholder="Weight">'
        + '</div>'
        + '</div>'
    )

}

function removeSet(currentEx, currentSet) {
    // TODO: Remove a set block from an exercise block
    set = document.getElementById('ex-'+ currentEx +'-set-'+ currentSet);
    set.remove();
}

function removeExercise(currentEx) {
    // TODO: Remove an exercise block
    ex = document.getElementById('ex-'+ currentEx);
    ex.remove();

    // Reduce exercise counter
    exercise--;
}