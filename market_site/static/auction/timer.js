window.onload = function() {
	let timer = document.querySelector("span[timer] b");
	let end_date = document.querySelector('td[end] span').textContent;
	// let countDownDate = new Date(end_date).getTime();
	let countDownDate = new Date(end_date);

	// Update the count down every 1 second
	let x = setInterval(function () {
		// Get today's date and time
		let now = new Date(Date.now());

		// Find the distance between now and the count down date
		let distance = countDownDate - now;

		// Time calculations for days, hours, minutes and seconds
		let days = Math.floor(distance / (1000 * 60 * 60 * 24));
		let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
		let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
		let seconds = Math.floor((distance % (1000 * 60)) / 1000);

		// Output the result in an element with id="demo"
		timer.innerHTML =
			days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

		// If the count down is over, write some text
		console.log(countDownDate, now, distance);
		if (distance < 0) {
			clearInterval(x);
			timer.innerHTML = "EXPIRED";
		}
	}, 1000);
	console.log(12);
}