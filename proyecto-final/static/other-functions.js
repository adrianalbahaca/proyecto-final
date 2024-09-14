function addSet(currentEx, currentSet){
    // TODO: Create a function that adds another set block to an exercise block
    var newSet = currentSet;
    newSet++;
    document.getElementById('ex-' + currentEx).insertAdjacentHTML('beforeend', '<div id="ex-'+ currentEx +'-set-'+ newSet +'">'
        + '<div class="row">'
        + '<div class="col d-flex flex-row">'
        + '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-arrow-return-right" viewBox="0 0 16 16">'
        + '<path fill-rule="evenodd" d="M1.5 1.5A.5.5 0 0 0 1 2v4.8a2.5 2.5 0 0 0 2.5 2.5h9.793l-3.347 3.346a.5.5 0 0 0 .708.708l4.2-4.2a.5.5 0 0 0 0-.708l-4-4a.5.5 0 0 0-.708.708L13.293 8.3H3.5A1.5 1.5 0 0 1 2 6.8V2a.5.5 0 0 0-.5-.5"/>'
        + '</svg>'
        + '<h3 class="ms-3">Set '+ newSet +'</h3>'
        + '</div>'
        + '<div class="col">'
        + '<input type="number" autocomplete="off" autofocus placeholder="Weight in KG" class="form-control" name="ex-'+ currentEx +'-set-'+ newSet +'-weight">'
        + '</div>'
        + '<div class="col">'
        + '<input type="number" autocomplete="off" autofocus placeholder="Reps" class="form-control" name="ex-'+ currentEx +'-set-'+ newSet +'-reps">'
        + '</div>'
        + '</div>'
        + '</div>'
    )

    document.getElementById('add-set-ex-'+ currentEx).setAttribute('onclick', 'addSet('+currentEx+', '+newSet+')');
    document.getElementById('remove-set-ex-' + currentEx).setAttribute('onclick', 'removeSet('+currentEx+', '+newSet+')');

}

function addExercise(currentEx) {
    // TODO: Create a new exercise block
    var newEx = currentEx;
    newEx++;
    
    document.getElementById('routine').insertAdjacentHTML('beforeend', '<div id="ex-'+ newEx +'">'
        + '<div class="row">'
        + '<!-- Exercise -->'
        + '<div class="col">'
        + '<h3>Exercise '+ newEx +'</h3>'
        + '</div>'
        + '<div class="col">'
        + '<input type="text" autocomplete="off" autocapitalize="on" autofocus class="form-control" name="ex-name-'+ newEx +'" placeholder="Exercise name">'
        + '</div>'
        + '<div class="col">'
        + '<div class="btn-group" role="group">'
        + '<p class="btn btn-outline-info" onclick="addSet('+ newEx +',1)" id="add-set-ex-'+ newEx +'">'
        + 'Add set'
        + '</p>'
        + '<p class="btn btn-outline-info" onclick="removeSet('+ newEx +',1)" id="remove-set-ex-'+ newEx +'">'
        + 'Remove set'
        + '</p>'
        + '<p class="btn btn-outline-warning" onclick="removeExercise('+ newEx +')" id="remove-ex-'+ newEx +'">'
        + 'Delete exercise'
        + '</p>'
        + '</div>'
        + '</div>'
        + '</div>'
        + '<!-- Sets -->'
        + '<div id="ex-'+ newEx +'-set-1">'
        + '<div class="row">'
        + '<div class="col d-flex flex-row">'
        + '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-arrow-return-right" viewBox="0 0 16 16">'
        + '<path fill-rule="evenodd" d="M1.5 1.5A.5.5 0 0 0 1 2v4.8a2.5 2.5 0 0 0 2.5 2.5h9.793l-3.347 3.346a.5.5 0 0 0 .708.708l4.2-4.2a.5.5 0 0 0 0-.708l-4-4a.5.5 0 0 0-.708.708L13.293 8.3H3.5A1.5 1.5 0 0 1 2 6.8V2a.5.5 0 0 0-.5-.5"/>'
        + '</svg>'
        + '<h3 class="ms-3">Set 1</h3>'
        + '</div>'
        + '<div class="col">'
        + '<input type="number" autocomplete="off" autofocus placeholder="Weight in KG" class="form-control" name="ex-'+ newEx +'-set-1-weight">'
        + '</div>'
        + '<div class="col">'
        + '<input type="number" autocomplete="off" autofocus placeholder="Reps" class="form-control" name="ex-'+ newEx +'-set-1-reps">'
        + '</div>'
        + '</div>'
        + '</div>'
        + '</div>'
    )

    document.getElementById('add-ex').setAttribute('onclick', 'addExercise('+ newEx +')')
    
}

function removeSet(currentEx, currentSet) {
    // TODO: Remove a set block from an exercise block
    set = document.getElementById('ex-'+ currentEx +'-set-'+ currentSet);
    set.remove();

    var backSet = currentSet;
    backSet--;
    document.getElementById('add-set-ex-' + currentEx).setAttribute('onclick', 'addSet('+ currentEx +', '+ backSet + ')');
    document.getElementById('remove-set-ex-' + currentEx).setAttribute('onclick', 'removeSet('+ currentEx +', '+ backSet +')');
}

function removeExercise(currentEx) {
    // TODO: Remove an exercise block
    ex = document.getElementById('ex-'+ currentEx);
    ex.remove();

    previousEx = currentEx;
    previousEx--;

    // Reduce exercise counter
    document.getElementById('add-ex').setAttribute('onclick', 'addExercise('+ previousEx +')');
}

// PR Shit

pr = 1;

function addPR() {
    // TODO: Add PR to the form
    // Add the new PR to the form
    document.getElementById('prs').insertAdjacentHTML('beforeend', '<div class="row" id="pr-' + pr + '">'
        + '<input type="text" name="ex-name-' + pr + '" id="">'
        + '<input type="text" name="ex-weight-'+ pr +'" id="">'
        + '<!-- Button to remove this pr -->'
        + '<h4 onclick="removePR('+ pr +')">-</h4>'
        + '</div>'
    )

    // Add 1 to the PR counter
    pr ++;
}

function removePR(currentPR) {
    // TODO: Remove PR of the form. Input being the PR to remove
    
    section = document.getElementById('pr-' + currentPR)
    section.remove()

    pr--;
}