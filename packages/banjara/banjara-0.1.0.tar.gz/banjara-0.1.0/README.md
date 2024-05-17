# Banjara - TUI Point of Sale

Banjara (terminal) is a text based point of sale system designed for simplicity

## Thesis

## Technology

- Textualize
- Stripe
- Tortoise ORM

## Stripe examples

```python
stripe.PaymentIntent.create(
  currency="aud",
  payment_method_types=["card_present"],
  capture_method="manual",
  amount=1998,
)
```

```python
stripe.terminal.Reader.process_payment_intent(
  "tmr_F",
  payment_intent="pi_3O",
)
```

```python
stripe.terminal.Reader.set_reader_display(
  "tmr_Fal",
  type="cart",
  cart={
    "line_items": [
      {"description": "Caramel latte", "amount": 659, "quantity": 1},
      {"description": "Dozen donuts", "amount": 1239, "quantity": 1},
    ],
    "currency": "aud",
    "tax": 100,
    "total": 1998,
  },
)
```

## License
