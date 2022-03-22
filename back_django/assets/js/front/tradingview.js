import { createChart } from 'lightweight-charts';
import axios from 'axios';

export async function tradingview() {

    const historicals = await getHistoricals()
    const candles = await historicalsToCandles(historicals)

    const tradingview = document.getElementById('tradingview')

    let chart = createChart(tradingview, {
        width: 1000,
        height: 500,
        layout: {
            backgroundColor: '#000',
            textColor: 'rgba(255, 255, 255, 0.7)',
        },
        grid: {
            vertLines: {
                color: 'rgba(197, 203, 206, 0.0)',
            },
            horzLines: {
                color: 'rgba(197, 203, 206, 0.0)',
            },
        },
        timeScale: {
            timeVisible: true,
            secondsVisible: false,
        },
    });

    const candlestickSeries = chart.addCandlestickSeries();

    candlestickSeries.setData(candles)

    // candlestickSeries.setData([
    //     { time: '2018-12-22', open: 75.16, high: 82.84, low: 36.16, close: 45.72 },
    //     { time: '2018-12-23', open: 45.12, high: 53.90, low: 45.12, close: 48.09 },
    //     { time: '2018-12-24', open: 60.71, high: 60.71, low: 53.39, close: 59.29 },
    //     { time: '2018-12-25', open: 68.26, high: 68.26, low: 59.04, close: 60.50 },
    //     { time: '2018-12-26', open: 67.71, high: 105.85, low: 66.67, close: 91.04 },
    //     { time: '2018-12-27', open: 91.04, high: 121.40, low: 82.70, close: 111.40 },
    //     { time: '2018-12-28', open: 111.51, high: 142.83, low: 103.34, close: 131.25 },
    //     { time: '2018-12-29', open: 131.33, high: 151.17, low: 77.68, close: 96.43 },
    //     { time: '2018-12-30', open: 106.33, high: 110.20, low: 90.39, close: 98.10 },
    //     { time: '2018-12-31', open: 109.87, high: 114.69, low: 85.66, close: 111.26 },
    // ]);
}

async function historicalsToCandles(historicalsString) {

    let historicals = JSON.parse(historicalsString)
    let candles = []

    historicals.forEach(historical => {
        let date = new Date(historical.fields.datetime)
        const unixTimestamp = Math.floor(date.getTime() / 1000);
        candles.push({
            time: unixTimestamp,
            open: historical.fields.open,
            high: historical.fields.high,
            low: historical.fields.low,
            close: historical.fields.close
        })
    });

    console.log(historicals);
    console.log(candles);

    return candles
}


async function getHistoricals() {
    const tradingviewContainer = document.querySelector('#tradingview_container')
    // @ts-ignore
    const requestUrl = tradingviewContainer.dataset.ajaxUrl

    const response = await axios.get(requestUrl);
    const candles = response.data;

    return candles

}