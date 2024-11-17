function deleteGame(gameId){
    fetch("/delete-game", {
        method:"POST",
        body: JSON.stringify({ gameId: gameId }),
    }).then ((_res) => {
        window.location.href = "/";
    });
}
function acceptGame(gameId){
    fetch("/accept-game", {
        method:"POST",
        body: JSON.stringify({ gameId: gameId }),
    }).then ((_res) => {
        window.location.href = "/";
    });
}