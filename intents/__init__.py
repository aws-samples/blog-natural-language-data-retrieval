from intents.context_specs import vacation
from intents.context_specs import coffee
from intents.context_specs import olympics

contexts = {
    vacation.INTENT_DESC: vacation,
    coffee.INTENT_DESC: coffee,
    olympics.INTENT_DESC: olympics
}
INTENT_UNKNOWN = "unknown"
