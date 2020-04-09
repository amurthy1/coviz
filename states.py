from coviz_helper import load_data, process_data, construct_doubling_text
import plotly.graph_objects as go


def plot_data_by_state(initial_state = "California"):
    states_df = load_data("us-states.csv")
    data_by_state = {}
    for state in states_df.state.unique():
        state_df = states_df[states_df.state == state]
        if len(state_df) > 2:
            data_by_state[state] = process_data(state_df)

    doubling_text = {}
    for state, state_data in data_by_state.items():
        doubling_text[state] = construct_doubling_text(
            state_data[1][-1], state_data[1][0], len(state_data[1])
        )

    states = sorted(list(data_by_state.keys()))

    fig = go.Figure()
    initial_data = data_by_state[initial_state]
    fig.add_trace(go.Scatter(x=initial_data[0], y=initial_data[1], name ='actual', mode='markers'))
    fig.add_trace(go.Scatter(x=initial_data[0], y=initial_data[2], name = 'model', mode='lines'))
    fig.update_layout(
        title=dict(
            text="Covid cases by state over time",
            x=0.5,
            xanchor="center",
            yanchor="top",
            y=1,
            pad={"t": 20}
        ),
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        args=[
                            {
                                "x": [data_by_state[state][0], data_by_state[state][0]],
                                "y": [data_by_state[state][1], data_by_state[state][2]],
                            },
                            {
                                "xaxis.title": doubling_text[state],
                            },
                        ],
                        label=state,
                        method="update",
                    )
                    for state in states
                ],
                active=states.index(initial_state),
                direction="down",
                pad={"r": 10, "t": -10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ],
        annotations=[
            dict(
                x=0.03,
                y=1.1,
                xref="paper",
                yref="paper",
                text="State:",
                showarrow=False,
                yanchor="top",
                xanchor="left",
                font=dict(size=13),
            ),
        ],
        height = 600,
        margin=dict(t=100),
        xaxis_title=doubling_text[initial_state],
        yaxis_title="# of cases",
    )

    fig.show()
