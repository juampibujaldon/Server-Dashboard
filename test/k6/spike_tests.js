import http from 'k6/http';
import { Trend } from 'k6/metrics';
import { check } from 'k6';

const statusTrend = new Trend('status_codes');

export const options = {
    stages: [
        { duration: '10s', target: 100 },
        { duration: '20s', target: 100 },
        { duration: '10s', target: 0 },
    ],
};

const BASE_URL = 'http://localhost:5001/api';
const payload = JSON.stringify({
    serverId: 'MSI',
    cpu_usage: 20.5,
    ram_usage: 55.3,
    disk_space: 40.0,
    temperature: 45.0,
});
const params = { headers: { 'Content-Type': 'application/json' } };

export default function () {
    const res = http.post(`${BASE_URL}/metrics`, payload, params);

    statusTrend.add(res.status);

    check(res, {
        'status 201': (r) => r.status === 201,
        // 'status 400': (r) => r.status === 400,
        // 'status 404': (r) => r.status === 404,
        // 'status 409': (r) => r.status === 409,
        // 'status 429': (r) => r.status === 429,
        // 'status 500': (r) => r.status === 500,
    });
}


