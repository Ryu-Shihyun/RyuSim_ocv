#ifndef NO_TRANSMIT_RATE_CONTROL_HPP
#define NO_TRANSMIT_RATE_CONTROL_HPP

#include <vanetza/common/clock.hpp>
#include <vanetza/dcc/burst_budget.hpp>
#include <vanetza/dcc/profile.hpp>
#include <vanetza/dcc/state_machine_budget.hpp>
#include <vanetza/dcc/transmit_rate_control.hpp>


namespace vanetza
{

// forward declarations
  class Runtime;
  namespace dcc { class StateMachine; }

  namespace dcc
  {

/**
 * Transmit Rate Control with occasional DP0 message bursts.
 * DP1, DP2 and DP3 messages are controlled by a state machine only.
 */
    class NoTransmitRateControl : public TransmitRateControl
    {
    public:
        NoTransmitRateControl(const StateMachine&, const Runtime& rt);

        Clock::duration delay(const Transmission&) override;
        Clock::duration interval(const Transmission&) override;
        void notify(const Transmission&) override;

    private:
        BurstBudget m_burst_budget;
        StateMachineBudget m_fsm_budget;
        const StateMachine& m_fsm;
    };

  } // namespace dcc
} // namespace vanetza

#endif NO_TRANSMIT_RATE_CONTROL_HPP

