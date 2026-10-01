from django.db import models


class Drug(models.Model):
    molecule_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    generic_name = models.CharField(
        max_length=255,
        db_index=True,
    )

    drug_class = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "drugs"

    def __str__(self):
        return f"{self.generic_name} ({self.molecule_id})"


class DrugAlias(models.Model):
    drug = models.ForeignKey(
        Drug,
        on_delete=models.CASCADE,
        related_name="aliases",
    )

    alias = models.CharField(
        max_length=255,
        db_index=True,
    )

    normalized_alias = models.CharField(
        max_length=255,
        db_index=True,
    )

    alias_type = models.CharField(
        max_length=50,
        default="generic",
    )

    source = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    class Meta:
        db_table = "drug_aliases"
        constraints = [
            models.UniqueConstraint(
                fields=["drug", "normalized_alias"],
                name="unique_drug_alias",
            )
        ]

    def __str__(self):
        return f"{self.alias} → {self.drug.generic_name}"


class DrugInteraction(models.Model):
    interaction_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    drug_a = models.ForeignKey(
        Drug,
        on_delete=models.CASCADE,
        related_name="interactions_as_a",
    )

    drug_b = models.ForeignKey(
        Drug,
        on_delete=models.CASCADE,
        related_name="interactions_as_b",
    )

    # Always store the lower Drug ID first.
    pair_key = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    severity = models.CharField(
        max_length=50,
        db_index=True,
    )

    description = models.TextField(
        blank=True,
        default="",
    )

    source = models.CharField(
        max_length=255,
    )

    source_record_id = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    kb_version = models.CharField(
        max_length=100,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "drug_interactions"

    def save(self, *args, **kwargs):
        if self.drug_a_id > self.drug_b_id:
            self.drug_a_id, self.drug_b_id = (
                self.drug_b_id,
                self.drug_a_id,
            )

        self.pair_key = f"{self.drug_a_id}:{self.drug_b_id}"

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.drug_a.generic_name} + "
            f"{self.drug_b.generic_name} "
            f"({self.severity})"
        )