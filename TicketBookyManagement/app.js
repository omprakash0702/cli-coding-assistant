const buses = [
    { name: 'Volvo', route: 'Delhi to Mumbai', timings: '10:00 AM' },
    { name: 'Neeta', route: 'Mumbai to Pune', timings: '11:00 AM' },
    { name: 'SRS', route: 'Bangalore to Chennai', timings: '12:00 PM' },
    { name: 'KPN', route: 'Chennai to Coimbatore', timings: '01:00 PM' },
    { name: 'VRL', route: 'Hyderabad to Goa', timings: '02:00 PM' },
    { name: 'KSRTC', route: 'Bangalore to Mysore', timings: '03:00 PM' },
    { name: 'RedBus', route: 'Delhi to Jaipur', timings: '04:00 PM' },
    { name: 'AbhiBus', route: 'Mumbai to Nashik', timings: '05:00 PM' },
    { name: 'Yatra', route: 'Kolkata to Durgapur', timings: '06:00 PM' },
    { name: 'GoBus', route: 'Ahmedabad to Surat', timings: '07:00 PM' },
    { name: 'Orange Travels', route: 'Pune to Nashik', timings: '08:00 PM' },
    { name: 'Chalo', route: 'Delhi to Agra', timings: '09:00 PM' },
    { name: 'TravelKhana', route: 'Jaipur to Udaipur', timings: '10:00 PM' },
    { name: 'Himachal Roadways', route: 'Shimla to Manali', timings: '11:00 PM' },
    { name: 'State Transport', route: 'Kerala to Tamil Nadu', timings: '12:00 AM' },
    { name: 'SRS Travels', route: 'Pune to Bangalore', timings: '01:00 AM' },
    { name: 'Maharashtra Travels', route: 'Mumbai to Aurangabad', timings: '02:00 AM' },
    { name: 'Karnataka Travels', route: 'Bangalore to Hubli', timings: '03:00 AM' },
    { name: 'Gujarat Travels', route: 'Ahmedabad to Vadodara', timings: '04:00 AM' }
];

const busSelect = document.getElementById('busOptions');
buses.forEach(bus => {
    const option = document.createElement('option');
    option.value = bus.name;
    option.textContent = `${bus.name} (${bus.route}, ${bus.timings})`;
    busSelect.appendChild(option);
});

document.getElementById('bookingForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const selectedBus = busSelect.value;
    const seats = document.getElementById('seats').value;
    document.getElementById('bookingConfirmation').textContent = `You have booked ${seats} seat(s) on ${selectedBus}.`;
});