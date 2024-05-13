from decimal import Decimal

import pandas as pd

from hummingbot.core.data_type.common import OrderType, TradeType
from hummingbot.strategy_v2.backtesting.executor_simulator_base import ExecutorSimulation, ExecutorSimulatorBase
from hummingbot.strategy_v2.executors.position_executor.data_types import PositionExecutorConfig
from hummingbot.strategy_v2.models.executors import CloseType


class PositionExecutorSimulator(ExecutorSimulatorBase):
    def simulate(self, df: pd.DataFrame, config: PositionExecutorConfig, trade_cost: float) -> ExecutorSimulation:
        if config.triple_barrier_config.open_order_type == OrderType.LIMIT:
            entry_condition = (df['close'] < config.entry_price) if config.side == TradeType.BUY else (df['close'] > config.entry_price)
            start_timestamp = df[entry_condition]['timestamp'].min()
        else:
            start_timestamp = df['timestamp'].min()
        last_timestamp = df['timestamp'].max()

        # Set up barriers
        tp = Decimal(config.triple_barrier_config.take_profit) if config.triple_barrier_config.take_profit else None
        sl = Decimal(config.triple_barrier_config.stop_loss) if config.triple_barrier_config.stop_loss else None
        tl = config.triple_barrier_config.time_limit * 1000 if config.triple_barrier_config.time_limit else None
        tl_timestamp = config.timestamp + tl if tl else last_timestamp

        # Filter dataframe based on the conditions
        df_filtered = df[df['timestamp'] <= tl_timestamp].copy()
        df_filtered['net_pnl_pct'] = 0.0
        df_filtered['net_pnl_quote'] = 0.0
        df_filtered['cum_fees_quote'] = 0.0
        df_filtered['filled_amount_quote'] = 0.0
        df_filtered["current_position_average_price"] = float(config.entry_price)

        if pd.isna(start_timestamp):
            return ExecutorSimulation(config=config, executor_simulation=df_filtered, close_type=CloseType.TIME_LIMIT)

        entry_price = df.loc[df['timestamp'] == start_timestamp, 'close'].values[0]

        returns_df = df_filtered[df_filtered['timestamp'] >= start_timestamp]
        returns = returns_df['close'].pct_change().fillna(0)
        cumulative_returns = (1 + returns).cumprod() - 1
        df_filtered.loc[df_filtered['timestamp'] >= start_timestamp, 'net_pnl_pct'] = cumulative_returns if config.side == TradeType.BUY else -cumulative_returns
        df_filtered.loc[df_filtered['timestamp'] >= start_timestamp, 'filled_amount_quote'] = float(config.amount) * entry_price
        df_filtered['net_pnl_quote'] = df_filtered['net_pnl_pct'] * df_filtered['filled_amount_quote']
        df_filtered['cum_fees_quote'] = trade_cost * df_filtered['filled_amount_quote']

        # Determine the earliest close event
        first_tp_timestamp = df_filtered[df_filtered['net_pnl_pct'] > tp]['timestamp'].min() if tp else None
        first_sl_timestamp = df_filtered[df_filtered['net_pnl_pct'] < -sl]['timestamp'].min() if sl else None
        close_timestamp = min([timestamp for timestamp in [first_tp_timestamp, first_sl_timestamp, tl_timestamp] if not pd.isna(timestamp)])

        # Determine the close type
        if close_timestamp == first_tp_timestamp:
            close_type = CloseType.TAKE_PROFIT
        elif close_timestamp == first_sl_timestamp:
            close_type = CloseType.STOP_LOSS
        else:
            close_type = CloseType.TIME_LIMIT

        # Set the final state of the DataFrame
        df_filtered = df_filtered[df_filtered['timestamp'] <= close_timestamp]

        # Construct and return ExecutorSimulation object
        simulation = ExecutorSimulation(
            config=config,
            executor_simulation=df_filtered,
            close_type=close_type
        )
        return simulation
