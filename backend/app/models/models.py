from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    predictions: Mapped[list["Prediction"]] = relationship(back_populates="user")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="user")
    feedback_entries: Mapped[list["Feedback"]] = relationship(back_populates="user")


class WasteCategory(Base):
    __tablename__ = "waste_categories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_biodegradable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    waste_items: Mapped[list["WasteItem"]] = relationship(back_populates="category")
    predictions: Mapped[list["Prediction"]] = relationship(
        foreign_keys="Prediction.predicted_category_id",
        back_populates="predicted_category",
    )
    corrected_feedback: Mapped[list["Feedback"]] = relationship(
        foreign_keys="Feedback.corrected_category_id",
        back_populates="corrected_category",
    )


class WasteItem(Base):
    __tablename__ = "waste_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("waste_categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    knowledge_subtype_slug: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    category: Mapped["WasteCategory"] = relationship(back_populates="waste_items")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="predicted_item")

    __table_args__ = (
        UniqueConstraint("category_id", "name", name="uq_waste_item_category_name"),
    )


class Microorganism(Base):
    __tablename__ = "microorganisms"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    scientific_name: Mapped[str] = mapped_column(String(255), nullable=False)
    common_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    microbial_type: Mapped[str] = mapped_column(String(50), nullable=False)
    taxonomic_group: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("scientific_name", "microbial_type", name="uq_microorganism_name_type"),
    )


class DecompositionProfile(Base):
    __tablename__ = "decomposition_profiles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    waste_subtype_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    treatment_method: Mapped[str] = mapped_column(String(100), nullable=False, default="aerobic composting", server_default="aerobic composting")
    compost_stage: Mapped[str | None] = mapped_column(String(50), nullable=True)
    temperature_min_c: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    temperature_max_c: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    moisture_min_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    moisture_max_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    ph_min: Mapped[Decimal | None] = mapped_column(Numeric(4, 2), nullable=True)
    ph_max: Mapped[Decimal | None] = mapped_column(Numeric(4, 2), nullable=True)
    cn_ratio_min: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    cn_ratio_max: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    expected_days_min: Mapped[int | None] = mapped_column(nullable=True)
    expected_days_max: Mapped[int | None] = mapped_column(nullable=True)
    evidence_scope: Mapped[str] = mapped_column(String(50), nullable=False, default="study_reported", server_default="study_reported")
    recommendation_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="decomposition_profile")


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    image_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    predicted_category_id: Mapped[int] = mapped_column(ForeignKey("waste_categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    predicted_item_id: Mapped[int | None] = mapped_column(ForeignKey("waste_items.id", ondelete="SET NULL"), nullable=True, index=True)
    confidence: Mapped[Decimal] = mapped_column(Numeric(6, 5), nullable=False)
    class_probabilities: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    model_name: Mapped[str] = mapped_column(String(120), nullable=False, default="MobileNetV3Small", server_default="MobileNetV3Small")
    model_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user: Mapped["User | None"] = relationship(back_populates="predictions")
    predicted_category: Mapped["WasteCategory"] = relationship(foreign_keys=[predicted_category_id], back_populates="predictions")
    predicted_item: Mapped["WasteItem | None"] = relationship(back_populates="predictions")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="prediction")
    feedback_entries: Mapped[list["Feedback"]] = relationship(back_populates="prediction")

    __table_args__ = (
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="chk_prediction_confidence"),
    )


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    prediction_id: Mapped[int] = mapped_column(ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False, index=True)
    decomposition_profile_id: Mapped[int | None] = mapped_column(ForeignKey("decomposition_profiles.id", ondelete="SET NULL"), nullable=True, index=True)
    recommendation_text: Mapped[str] = mapped_column(Text, nullable=False)
    scientific_basis: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user: Mapped["User | None"] = relationship(back_populates="recommendations")
    prediction: Mapped["Prediction"] = relationship(back_populates="recommendations")
    decomposition_profile: Mapped["DecompositionProfile | None"] = relationship(back_populates="recommendations")
    feedback_entries: Mapped[list["Feedback"]] = relationship(back_populates="recommendation")


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    prediction_id: Mapped[int] = mapped_column(ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False, index=True)
    recommendation_id: Mapped[int | None] = mapped_column(ForeignKey("recommendations.id", ondelete="SET NULL"), nullable=True, index=True)
    corrected_category_id: Mapped[int | None] = mapped_column(ForeignKey("waste_categories.id", ondelete="SET NULL"), nullable=True, index=True)
    rating: Mapped[int | None] = mapped_column(nullable=True)
    was_prediction_correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user: Mapped["User | None"] = relationship(back_populates="feedback_entries")
    prediction: Mapped["Prediction"] = relationship(back_populates="feedback_entries")
    recommendation: Mapped["Recommendation | None"] = relationship(back_populates="feedback_entries")
    corrected_category: Mapped["WasteCategory | None"] = relationship(
        foreign_keys=[corrected_category_id],
        back_populates="corrected_feedback",
    )

    __table_args__ = (
        CheckConstraint("rating IS NULL OR (rating >= 1 AND rating <= 5)", name="chk_feedback_rating"),
    )
