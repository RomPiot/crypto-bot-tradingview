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