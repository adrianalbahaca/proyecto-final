let currentExercise = 1

function addSet(currentSet, exerciseSet) {
    // TODO: Find the box where the section is and add a new set on the block
    // Let's get the current set on a number parsed into the function
    let nextSet = currentSet + 1;

    // Then we could use it to add a new div block with the new number
    document.getElementById('exercise-' + exerciseSet).insertAdjacentHTML("beforeend", `<div class="set" id="set-${nextSet}"><h3>Set ${nextSet}</h3><input type="text" name="ex-${currentExercise}-set-${nextSet}-reps" id=""><input type="text" name="ex-${currentExercise}-set-${nextSet}-weight" id=""></div>`)

    // Change the button's 'onclick' attribute
    document.getElementById('add-set-' + currentSet).setAttribute('onclick', 'addSet(' + nextSet + ', ' + exerciseSet + ')')
}

function addExercise() {
    // TODO: Insert a new div for a new exercise in the routine
    // Let's get the counter for the next exercise
    currentExercise += 1;

    // Then we add a new div block with the new number
    document.getElementById('routine').insertAdjacentHTML("beforeend", `<div class="exercise" id="exercise-${currentExercise}"><input type="text" name="exercise-name-${currentExercise}" id=""><div class="set" id="set-1"><h3>Set 1</h3><input type="text" name="ex-${currentExercise}-set-1-reps" id=""><input type="text" name="ex-${currentExercise}-set-1-weight" id=""></div></div><div class="add-set-1"><h3 onclick="addSet(1, ${currentExercise})" id="add-set">Add set</h3></div>`)

    // Change the 'onclick' attribute on the button
    document.getElementById('add-exercise').setAttribute('onclick', `addExercise(${currentExercise})`)
}

function removeExercise() {
    // TODO: Create a function that removes the previous block of exercises, including its sets

}

function removeSet() {
    // TODO: Create a function that removes the previous set
}